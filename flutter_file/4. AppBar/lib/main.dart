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
        appBar: AppBar(title: Text('카메라')),
        body: SizedBox(
          child: Text('안녕하세요',
            //style: TextStyle(color: Color(0xffad4444)),),   // Color(0xffaaaaa)을 사용하면 옆에 생긴 사각형에서 색을 선택할 수 있음
            //style: TextStyle(color: Color.fromRGBO(r, g, b, opacity)),
            style: TextStyle(letterSpacing: 30, fontWeight: FontWeight.w700),              // letterSpacing : 자간 조정, fontWeight : 두께 조정 0~900
          ),                                 // child: Icon(Icons.star, color: , size: ) 이렇게 아이콘도 가능
        ),
      ),
    );
  }
}
