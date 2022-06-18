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
        appBar: AppBar(title: Text('앱임')),

        body: Align(
          alignment: Alignment.bottomCenter,            // 박스 위치 선정은 Align(alignment: )를 사용
          child: Container(
            width: double.infinity, height: 50, color: Colors.blue,     // double.infinity : 길이를 무한히 주어라
            //margin: EdgeInsets.all(20),                  // 박스에 바깥 여백을 주는 방법
            margin: EdgeInsets.fromLTRB(0, 30, 0, 0),         // 여백의 위치 조정
            //padding: EdgeInsets.all(20),                 // 박스 안쪽 여백을 주는 방법
            child: Text('A'),                                 // 만약 padding이 없으면 박스의 왼쪽 상단부터 글이 채워짐
            //decoration: BoxDecoration(
              //border: Border.all(color: Colors.black)      // 나머지 옵션은 decoration을 사용하는데 이럴 경우 색을 두가지 지정하기 위해서는 에러 메시지를 구글에 검색

            ),
        ),

        ),
      );
  }
}
