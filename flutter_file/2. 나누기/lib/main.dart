import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {   // 자동완성은 ctrl + space

    return MaterialApp(                   // ui 디자인하기 위해서 MaterialApp 사용
      home: Scaffold(                       // Scaffold : 상중하로 나누기
        appBar: AppBar(),                      // appBar : 상단에 들어갈 위젯
        body: Row(                       // body : 중단에 들어갈 위젯      Row : 여러가지 위젯을 가로로 배치
          mainAxisAlignment:  MainAxisAlignment.spaceBetween,     // 가로축으로 정렬 방법
          crossAxisAlignment: CrossAxisAlignment.center,          // 세로축으로 정렬 방법
          children: [                          // 이런 경우에는 child가 아닌 children
            Icon(Icons.star),                  // Column : 여러가지 위젯을 세로로 배치
            Icon(Icons.star)
          ],
        ),
        bottomNavigationBar: BottomAppBar( child: Text('뒤로'), ),   // bottomNavigationBar : 하단에 들어갈 위젯
      )
    );
  }
}
