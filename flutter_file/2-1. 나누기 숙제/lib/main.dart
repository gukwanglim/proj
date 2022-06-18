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
        appBar: AppBar(title: Text('앱임'),),
        body: Text('안녕'),
        bottomNavigationBar: BottomAppBar(
          child: SizedBox(                           // Container는 살짝 무거움
            height: 70,                              // sizebox는 width, height, child만 필요할 경우 사용
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Icon(Icons.phone),
                Icon(Icons.message),
                Icon(Icons.contact_page)
              ],
            ),
          )
        ),
        ),
      );
  }
}
