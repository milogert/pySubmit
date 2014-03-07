function addUser(theEvent) {
  var aUsername = $("#newUsername").val();
  var aPassword = $("#newPassword").val();
  var aRole = $("#newRole").val();

  // Ajax call.
  var aRequest = $.ajax({
    url: "/api/addUser",
    type: "POST",
    data: {
      theUsername: aUsername,
      thePassword: aPassword,
      theRole: aRole
    }
  });

  aRequest.done(function(msg) {
    console.log(msg);
  }); //(flashCurrentRow);

  aRequest.fail(function() {
    console.log("Dead.");
  })
}

function showEdit(theEvent) {
  $(this).append($("<span class='glyphicon glyphicon-pencil' style='float: right;'></span>"));
}

function hideEdit(theEvent) {
  $(this).find("span:last").remove();
}

function editRow(theEvent) {
  var aParent = $(this).parent().find("td:not(:last)");
  var aButton = $(this).parent().find("td:last").find("button");

  for (var i = aParent.length - 1; i >= 0; i--) {
    var aEle = $(aParent[i]);
    var aText = aEle.text();
    aEle.html("<input type='text' class='form-control' value=" + aText + ">");
    aEle.off("click mouseenter mouseleave");
  };

  aButton.find("span").attr("class", "glyphicon glyphicon-floppy-save");
  // aButton.removeClass("remove").addClass("save");
  aButton.off("click");
  aButton.on("click", saveRow);
}

function saveRow(theEvent) {
  // Grab all the values from the form.
  var aParent = $(this).parent().parent().find("td:not(:last)");
  var aUser = ["", "", ""];

  // Get new values and reset the page.
  for (var i = aParent.length - 1; i >= 0; i--) {
    var aEle = $(aParent[i]);
    aUser[i] = aEle.find("input").val();
    aEle.on("click", editRow);
    aEle.on("mouseenter", showEdit);
    aEle.on("mouseleave", hideEdit);
    aEle.html(aUser[i]);
  };

  // Ajax call.
  var aRequest = $.ajax({
    url: "/api/editUser",
    type: "POST",
    data: {
      theUsername: aUser[0],
      thePassword: aUser[1],
      theRole: aUser[2]
    }
  });

  aRequest.done(function(msg) {
    console.log(msg);
  }); //(flashCurrentRow);

  aRequest.fail(function() {
    console.log("Dead.");
  })

  $(this).off("click");
  $(this).on("click", removeRow);
  $(this).find("span").attr("class", "glyphicon glyphicon-remove");

}

function removeRow(theEvent) {
  var aUser = $(this).parent().siblings(".username").text();

  // Ajax call.
  var aRequest = $.ajax({
    url: "/api/deleteUser",
    type: "POST",
    data: {
      theUsername: aUser
    }
  });

  aRequest.done(function(theMsg) {
    console.log(theMsg);
  }); //(flashCurrentRow);

  aRequest.fail(function(theMsg) {
    console.log(theMsg);
  })

  $(this).parent().parent().remove()
}

function flashCurrentRow(theEvent) {
  // Flash the row.
}

$(function() {
  // Setup handlers.
  $(".edit").hover(showEdit, hideEdit);

  $(".edit").click(editRow);

  $(".btn-edit").on("click", removeRow)

  $("#btn-add").on("click", addUser);
});