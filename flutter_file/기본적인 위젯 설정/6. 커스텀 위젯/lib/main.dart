import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(),
        body: ListView(                         // Column 을 사용하면 아무리 내용이 많아도 스크롤바가 생기지 않음
          children: [                                  // 스크롤바를 만들기 위해서는 Column 대신에 ListView를 사용
            Text('안녕'),
            Text('안녕'),
            Text('안녕'),
            Text('안녕'),
            Text('안녕'),
          ]
        ),
        bottomNavigationBar: BottomAppBar(),
      ),
    );
  }
}

class ShopItem extends StatelessWidget {              // 커스텀 함수(class) 만드는 법
  const ShopItem({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {

    return SizedBox(
      child: Text('안녕'),
    );
  }
}

var a = SizedBox(                                   // 함수로 만드는 법
  child: Text('안녕'),                                     // 함수의 경우는 변하는(변수가 포함되는) 것들에 사용하면 에러 가능성 발생
);
