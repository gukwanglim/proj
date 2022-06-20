import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'edit.dart';
import '../database/db.dart';
import '../database/memo.dart';


class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  //int _counter = 0;

  //void _incrementCounter() {
    //setState(() {
      //_counter++;
   // });
 // }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      body: ListView(
        physics: BouncingScrollPhysics(),
        children: [
          Row(
            children: [
              Padding(padding: EdgeInsets.only(left: 20, top: 20, bottom: 20),
              child: Text('메모메모', style: TextStyle(fontSize: 30,
                  color: Colors.blue),),)
            ],
          ),
          ...LoadMemo()
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: (){
          Navigator.push(                                    // screens 안의 edit.dart로 연결시켜주는 부분
            context,                               // context는 위의 Widget build(BuildContext context)에서 받아옴
            CupertinoPageRoute(builder: (context) => EditPage())        // EditPage는 edit.dart에서 작성
          );
        },
        tooltip: '메모를 추가하려면 클릭하세요',
        label: Text('메모 추가'),
        icon: Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }

  List<Widget> LoadMemo() {
    List<Widget> memoList = [];
    memoList.add(Container(color: Colors.redAccent, height: 100,));
    memoList.add(Container(color: Colors.orange, height: 100,));
    memoList.add(Container(color: Colors.yellow, height: 100,));
    memoList.add(Container(color: Colors.green, height: 100,));
    memoList.add(Container(color: Colors.blue, height: 100,));
    memoList.add(Container(color: Colors.indigo, height: 100,));
    memoList.add(Container(color: Colors.purpleAccent, height: 100,));
    return memoList;
  }

  Future<List<Memo>> loadMemo() async {
    DBHelper sd = DBHelper();          // 여기서 sd는 sqldatabase를 말하는 것
    return await sd.memos();
  }
}
