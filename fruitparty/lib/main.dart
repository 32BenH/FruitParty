import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:flutter_statusbarcolor/flutter_statusbarcolor.dart';

void main() {
  runApp(Bananalyzer());
}

class Bananalyzer extends StatelessWidget {
  WebViewController _controller;

  @override
  Widget build(BuildContext context) {
    FlutterStatusbarcolor.setStatusBarColor(Colors.white);
    return MaterialApp(
      title: 'Bananalyzer',
      theme: ThemeData(
        //  primarySwatch: Colors.white,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: SafeArea(
        child: WebView(
          initialUrl: 'http://192.168.1.24:5000/',
          onWebViewCreated: (WebViewController webViewController) {
            _controller = webViewController;
          },
          javascriptMode: JavascriptMode.unrestricted,
          gestureNavigationEnabled: true,
        ),
      ),
    );
  }
}
