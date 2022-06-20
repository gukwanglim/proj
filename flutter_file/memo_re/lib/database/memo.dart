class Memo{
  final String? id;                        // final을 사용하여 선언하는 것인 듯
  final String? title;                    // final 뒤에 나오는 것은 어떤 종류의 정보를 받을지(int, string)
  final String? text;                     // int, string 다음에 나오는 것은 내가 선언하고자 하는 내용의 title
  final String? createTime;
  final String? editTime;                              // String 다음에 ?를 넣어줘야 null 값이 들어가도 정상적으로 작동

  Memo({this.id, this.title, this.text, this.createTime, this.editTime});

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'text': text,
      'createTime': createTime,
      'editTime': editTime
    };
  }

// 각 memo 정보를 보기 쉽도록 print 문을 사용하여 toString을 구현
  @override
  String toString() {
    return 'Memo{id: $id, title: $title, text: $text, createTime: $createTime, editTime: $editTime}';
  }
}