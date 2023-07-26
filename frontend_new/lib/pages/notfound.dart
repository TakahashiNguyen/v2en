import 'package:flutter/material.dart';
import 'package:vrouter/vrouter.dart';

class Error404Page extends StatelessWidget {
  const Error404Page({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.blue,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                '404',
                style: TextStyle(
                  fontSize: 30.0,
                  color: Colors.white,
                ),
              ),
              Text(
                'Oops. Nothing here...',
                style: TextStyle(
                  fontSize: 20.0,
                  color: Colors.white.withOpacity(0.4),
                ),
              ),
              const SizedBox(height: 20.0),
              ElevatedButton(
                onPressed: () => context.vRouter.to('/'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  elevation: 0.0,
                ),
                child: const Text(
                  'Go Home',
                  style: TextStyle(
                    color: Colors.blue,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
