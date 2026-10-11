import 'package:flutter_test/flutter_test.dart';
import 'package:moneymind/transaction_parser.dart';
void main() {
 test('parses debit',(){final t=TransactionParser.parse('Your account debited by Rs. 1,250.00 for payment to AMAZON');expect(t, isNotNull);expect(t!.amount,1250);expect(t.kind,TxKind.expense);});
 test('parses credit',(){final t=TransactionParser.parse('INR 500 credited to account from salary');expect(t,isNotNull);expect(t!.kind,TxKind.income);});
 test('rejects failed transaction',(){expect(TransactionParser.parse('Payment failed Rs 500 paid to merchant'),isNull);});
 test('rejects ambiguous message',(){expect(TransactionParser.parse('Your balance is Rs 500'),isNull);});
}
