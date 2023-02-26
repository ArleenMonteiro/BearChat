from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="landing.css" />
    <title>Document</title>
  </head>
  <body data-spy="scroll" data-target=".navbar" data-offset="50">
    <div class="wrapper">

    <div class="navbar">
      <div class="nav-items">
          <img src="paws.png" style="width: 50px;">
         
      </div>
      
  </div>

    <div id="home" class="con-l-1">
      <div id="main-title">
        <span id="title"> BearChat </span> <br />
        With your personal voice assisstant: Yucy <br />
        <br />
        <a href="app.html"><button class="button-32">Try it!</button></a>
      </div>
    

     
    </div>

    

    <div id="'info" class="con-l-1">
      <div id="info-main">


      </div>

    </div>
  </body>
</html>
"""
