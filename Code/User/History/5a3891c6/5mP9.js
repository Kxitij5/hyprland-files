var app = angular.module("cgpaApp", []);
app.controller("cgpaController", function ($scope) {
  $scope.users = [];
  $scope.cgpa = 0;

  $scope.addUser = function () {
    $scope.users.push({
      subject: $scope.subject,
      marks: $scope.marks,
      credit: $scope.credit,
    });
    $scope.calculateCgpa();
    $scope.subject = "";
    $scope.marks = "";
    $scope.credit = "";
  };

  $scope.calculateCgpa = function () {
    var sum = 0;
    var totalCredit = 0;

    for (var i = 0; i < $scope.users.length; i++) {
      var user = $scope.users[i];

      var gradePoints = getGradePoints(user.marks);

      sum += gradePoints * user.credit;
      totalCredit += user.credit;
    }

    $scope.cgpa = sum / totalCredit;
  };

  $scope.editUser = function (user) {
    var index = $scope.users.indexOf(user);

    var updatedName = prompt("Enter updated subject name:", user.subject);
    var updatedMarks = prompt("Enter updated marks:", user.marks);
    var updatedCredit = prompt("Enter updated credit:", user.credit);

    if (
      !(updatedName == null && updatedMarks == null && updatedCredit == null)
    ) {
      $scope.users.splice(index, 1, {
        subject: updatedName,
        marks: parseInt(updatedMarks),
        credit: parseInt(updatedCredit),
      });
      $scope.calculateCgpa();
    }
  };

  $scope.deleteUser = function (user) {
    var index = $scope.users.indexOf(user);
    $scope.users.splice(index, 1);
    $scope.calculateCgpa();
  };

  $scope.showConfetti = function () {
    if ($scope.cgpa > 8.5) {
      document.getElementById("confetti-container").innerHTML = "";

      var confettiElements = [];

      for (var i = 0; i < 100; i++) {
        confettiElements.push(createConfettiElement());
      }

      var container = document.getElementById("confetti-container");
      confettiElements.forEach(function (element) {
        container.appendChild(element);
      });

      animateConfetti(confettiElements);
    }
  };

  function createConfettiElement() {
    var confetti = document.createElement("div");
    confetti.classList.add("confetti");

    confetti.style.left = Math.random() * document.body.offsetWidth + "px";
    confetti.style.top = Math.random() * -100 + "px";
    confetti.style.backgroundColor = randomColor();

    return confetti;
  }

  function randomColor() {
    return `rgb(${Math.floor(
      Math.random() * 255
    )}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`;
  }

  function animateConfetti(confettiElements) {
    var animationDuration = 1500;
    var animationEasing = "ease-in-out";

    confettiElements.forEach(function (element) {
      element.style.animation = `confetti-fall ${animationDuration}ms ${animationEasing} infinite`;
    });
  }

  $scope.calculateCgpa();
});
function getGradePoints(marks) {
  if (marks >= 90) {
    return 10;
  } else if (marks <= 89 && marks >= 80) {
    return 9;
  } else if (marks <= 79 && marks >= 70) {
    return 8;
  } else if (marks <= 69 && marks >= 60) {
    return 7;
  } else if (marks <= 59 && marks >= 50) {
    return 6;
  } else if (marks <= 49 && marks >= 45) {
    return 5;
  } else if (marks <= 44 && marks >= 40) {
    return 4;
  } else {
    return 0;
  }
}
