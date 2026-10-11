enum TxKind { income, expense }
class ParsedTransaction {
  final double amount; final TxKind kind; final String merchant, source, fingerprint;
  const ParsedTransaction({required this.amount, required this.kind, required this.merchant, required this.source, required this.fingerprint});
}
class TransactionParser {
  static final _amount = RegExp(r'(?:INR|Rs\\.?|₹)\\s*([0-9,]+(?:\\.[0-9]{1,2})?)|([0-9,]+(?:\\.[0-9]{1,2})?)\\s*(?:INR|Rs\\.?|₹)', caseSensitive:false);
  static final _debit = RegExp(r'\\b(debited|spent|paid|purchase|withdrawn|sent|transferred to)\\b',caseSensitive:false);
  static final _credit = RegExp(r'\\b(credited|received|deposited|refund(ed)?|salary|cashback|transferred from)\\b',caseSensitive:false);
  static final _failed = RegExp(r'\\b(failed|declined|reversed|cancelled|canceled|unsuccessful)\\b',caseSensitive:false);
  static ParsedTransaction? parse(String text,{String source='notification'}) {
    if (_failed.hasMatch(text)) return null;
    final m=_amount.firstMatch(text); if(m==null)return null;
    final amount=double.tryParse((m.group(1)??m.group(2)??'').replaceAll(',',''));
    if(amount==null||amount<=0)return null;
    final debit=_debit.hasMatch(text), credit=_credit.hasMatch(text);
    if(debit==credit)return null;
    final merchant=RegExp(r'(?:to|at|from|towards)\\s+([A-Z0-9][A-Z0-9 &._-]{1,35})',caseSensitive:false).firstMatch(text)?.group(1)?.trim() ?? (credit?'Money received':'Payment');
    return ParsedTransaction(amount:amount,kind:credit?TxKind.income:TxKind.expense,merchant:merchant,source:source,fingerprint:'${credit?'in':'out'}|${amount.toStringAsFixed(2)}|${text.toLowerCase().replaceAll(RegExp(r"\\s+")," ").trim().hashCode}');
  }
}
