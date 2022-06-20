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
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.only(left: 20, top: 20, bottom: 20),
            child: Text(
              '메모메모',
              style: TextStyle(fontSize: 30, color: Colors.blue),
            ),
          ),
          
          Expanded(child: memoBuilder())       // FutureBuilder를 사용하기 위해서 Expanded 사용
          
        ],
      ),

      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
              // screens 안의 edit.dart로 연결시켜주는 부분
              context, // context는 위의 Widget build(BuildContext context)에서 받아옴
              CupertinoPageRoute(
                  builder: (context) => EditPage()) // EditPage는 edit.dart에서 작성
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
    memoList.add(Container(
      color: Colors.redAccent,
      height: 100,
    ));
    memoList.add(Container(
      color: Colors.orange,
      height: 100,
    ));
    memoList.add(Container(
      color: Colors.yellow,
      height: 100,
    ));
    memoList.add(Container(
      color: Colors.green,
      height: 100,
    ));
    memoList.add(Container(
      color: Colors.blue,
      height: 100,
    ));
    memoList.add(Container(
      color: Colors.indigo,
      height: 100,
    ));
    memoList.add(Container(
      color: Colors.purpleAccent,
      height: 100,
    ));
    return memoList;
  }

  Future<List<Memo>> loadMemo() async {                                  // sqldatabase에서 데이터 가져오기(db.dart에 있음)
    DBHelper sd = DBHelper(); // 여기서 sd는 sqldatabase를 말하는 것
    return await sd.memos();
  }

  Widget memoBuilder() {                                                // 위에서 Expanded한 memoBuilder에 FutureBuilder 적용
    return FutureBuilder(
      builder: (context, Snap) {
        if ((Snap.data as List).isEmpty) {                               // isEmpty를 사용하기 위해서는 일단 null(여기서는 단순 null이 아닌 [] 값)이 아니어야한다
          //print('project snapshot data is: ${projectSnap.data}');       // 유튜브에서는 Snap.data가 list로 반환된다고 했는데 이제는 as List를 사용해야 list로 반환
          return Container(child: Text('메모를 지금바로 추가해보세요'),);
        }
        return ListView.builder(
          itemCount: (Snap.data as List).length,            // length에 null 값이 들어가면 안되기 때문에 (Snap.data as List)로 넣어준다
          itemBuilder: (context, index) {
            Memo memo = (Snap.data as List)[index];              // 여기도 마찬가지, [index] 앞에 . 이 없어야한다.
            return Column(
              children: [
                Text(memo.title.toString()),
                Text(memo.text.toString()),
                Text(memo.createTime.toString()),
                // Widget to display the list of project
              ],
            );
          },
        );
      },
      future: loadMemo(),
    );
  }
}
