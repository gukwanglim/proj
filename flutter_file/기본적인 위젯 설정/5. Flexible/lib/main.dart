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
        body: Column(
          children: [
            Flexible(child: Container(color: Colors.blue,), flex: 5,),           // 화면 비율로 설정하고 싶은 경우 Flexible 사용
            Flexible(child: Container(color: Colors.red,), flex: 5,),
            Expanded(child: Container(color: Colors.green))                      // Expanded : 화면 비율을 1만큼 가지고 있는 것

          ],
        ),
      )
    );
  }
}
