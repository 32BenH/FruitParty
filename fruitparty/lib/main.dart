import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:flutter_statusbarcolor/flutter_statusbarcolor.dart';

void main() {
  runApp(BananalyzerApp());
}

class BananalyzerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    FlutterStatusbarcolor.setStatusBarColor(Colors.white);
    return MaterialApp(
      title: "Bananalyzer",
      theme: ThemeData(
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: BananalyzerHomePage(title: "Bananalyzer Home"),
    );
  }
}

class BananalyzerHomePage extends StatefulWidget {
  BananalyzerHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _BananalyzerHomePageState createState() => _BananalyzerHomePageState();
}

class _BananalyzerHomePageState extends State<BananalyzerHomePage> {
  WebViewController _controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Bananalyzer"),
        leading: GestureDetector(
          onTap: () async {
            await Permission.camera.request();
          },
          child: Icon(Icons.camera),
        ),
      ),
      body: SafeArea(
        child: WebView(
          initialUrl: "https://www.bananalyzer.tech/",
          onWebViewCreated: (WebViewController webViewController) {
            _controller = webViewController;
          },
          javascriptMode: JavascriptMode.unrestricted,
          gestureNavigationEnabled: true,
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          _controller.clearCache();
        },
        tooltip: "Clear cache",
        child: Icon(Icons.refresh),
      ),
    );
  }
}
