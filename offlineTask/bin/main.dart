import 'package:offlineTask/FaceTask.dart';



main(List<String> args) async {
  FaceTask faceTask=new FaceTask("face-pp",false);
  await faceTask.Demon(5);
  print("done");
}



