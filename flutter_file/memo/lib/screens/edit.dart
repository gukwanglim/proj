import 'package:flutter/material.dart';
import '../database/db.dart';
import '../database/memo.dart';
import 'package:crypto/crypto.dart';
import 'dart:convert';

class EditPage extends StatelessWidget {
  String title = '';                       // 변수를 database에 전달하기 위해서 선언
  String text = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          actions: [
            IconButton(onPressed: () {}, icon: Icon(Icons.delete)),
            IconButton(onPressed: saveDB, icon: Icon(Icons.save))
          ],
        ),
        body: Padding(
          padding: EdgeInsets.all(20),
          child: Column(
            children: [
              TextField(
                onChanged: (String title) {this.title = title;},               // onChanged : 내용이 바뀌면 뒤에 나오는 함수 실행. 즉, title을 변경하면 위에서 선언했던 String title = ''; 부분에 전달
                style: TextStyle(fontSize: 30, fontWeight: FontWeight.w500),
                keyboardType: TextInputType.multiline,
                maxLines: null,
                //obscureText: true,                   // 비밀번호를 작성할 때, 암호화
                decoration: InputDecoration(hintText: '제목을 적어주세요'),
              ),
              Padding(padding: EdgeInsets.all(10)),
              TextField(
                onChanged: (String title) {this.title = title;},
                keyboardType: TextInputType.multiline,
                maxLines: null,
                //obscureText: true,                   // 비밀번호를 작성할 때, 암호화
                decoration: InputDecoration(hintText: '내용을 적어주세요'),
              ),
            ],
          ),
        ));
  }

  Future<void> saveDB() async {
    DBHelper sd = DBHelper();

    var fido = Memo(
      id: Str2Sha512(DateTime.now().toString()),
      title: this.title,
      text: this.text,
      createTime: DateTime.now().toString(),      // DateTime.now()를 불러와서 toString()을 사용하여 string으로 변환
      editTime: DateTime.now().toString()
    );

    await sd.insertMemo(fido);

    print(await sd.memos());        // 없어도 되는 부분으로, 저장한 데이터가 잘 저장되어있는지 확인하는 구문
  }                                 // 제대로 동작을 한다면 아래 Run 부분에 출력

  String Str2Sha512(String text) {
    var bytes = utf8.encode(text); // data being hashed

    var digest = sha512.convert(bytes);

    return digest.toString();
  }
}

