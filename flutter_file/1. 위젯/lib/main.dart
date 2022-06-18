import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());    // 앱을 시작해주세요  여기서는 'MyApp'의 위치에 앱 메인페이지를 입력
}

// stless를 적은 다음 tab키  ->  메인 페이지 세팅
class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
                                           // 여기까지는 기본적으로 작성해야하는 부분                                               // 이미지를 넣을 때는 asset 파일을 만들고 이미지를 옮긴 후,
    return MaterialApp(                      // 위젯을 넣는 부분 :                                                              // pubspec.yaml파일(앱을 만들 때 모든 자료가 들어가는 곳, 패키지, 라이브러리도 포함)에 들어가
      //home: Text('안녕')                 // 글자를 넣을 때 = Text('내용')                                                      // flutter(두 개가 있는데 아래에 있는 곳에) 아래 assets: 이라 적기, 그 아래 - assets/ 이라고 적으면 asset파일 안의 모든 것이라는 뜻
      //home: Icon(Icons.camera)          // 아이콘을 넣을 때 = Icon(Icons.아이콘 이름) 아이콘 이름은 flutter 홈페이지 참조
      //home: Image.asset('assets/KakaoTalk_20220617_224604427.jpg')          // 이미지를 넣을 때 = Image.asset('경로')
      //home: Container( width: 50, height: 50, color: Colors.blue )               // 네모 박스 넣을 때 = Container() 혹은 SizedBox()      크기의 단위는 LP로 50LP는 대략 1.2cm
      home: Center(
        child: Container( width: 50, height: 50, color: Colors.blue ),            // 위의 경우는 위치를 지정하지 않아 화면 전체가 박스로 나옴


      )
    );
  }
}
