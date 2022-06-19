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
        appBar: AppBar(actions: [Icon(Icons.star)], leading: Icon(Icons.menu),),              // leading: 을 통해 왼쪽에 아이콘을 넣을수도 있다.
        body: SizedBox(                                            // actions: [] 를 통해 오른쪽에 아이콘 넣기
          child: ElevatedButton(                       // TextButton(ElevatedButton으로 대체 가능) 에는 child, onPressed 필수
            child: Text('글자'),
            onPressed: (){},                          // IconButton 사용 시, Icon: 파라미터가 필요
            style: ButtonStyle(),),
        ),
      ),
    );
  }
}
        // 1. 예시 디자인 준비
        // 2. 네모로 보이는 건 모두 네모 그리기
        // 3. 바깥 네모부터 하나하나 위젯으로 그리기
        // 4. 마무리 디자인