import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());    // 앱을 시작해주세요  여기서는 'MyApp'의 위치에 앱 메인페이지를 입력
}

// stless를 적은 다음 tab키  ->  메인 페이지 세팅
class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
                                           // 여기까지는 기본적으로 작성해야하는 부분
    return MaterialApp(
      home: Text('안녕')                // 위젯을 넣는 부분 : 글자를 넣을 때 = Text('내용')
      home: Icon(Icons.shop)          // 아이콘을 넣을 때 = Icon(Icons.아이콘 이름) 아이콘 이름은 flutter 홈페이지 참조
      home: Image.asset('경로')
    );
  }
}
