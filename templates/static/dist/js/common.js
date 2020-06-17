(function ($) {
    $.fn.buttonLoader = function (action) {
        var self = $(this);
        //start loading animation
        if (action == 'start') {
            if ($(self).attr("disabled") == "disabled") {
                e.preventDefault();
            }
            //disable buttons when loading state
            $('.has-spinner').attr("disabled", "disabled");
            $(self).attr('data-btn-text', $(self).text());
            //binding spinner element to button and changing button text
            $(self).html('<span class="spinner"><i class="fas fa-spinner fa-spin"></i></span>Loading');
            $(self).addClass('active');
        }
        //stop loading animation
        if (action == 'stop') {
            $(self).html($(self).attr('data-btn-text'));
            $(self).removeClass('active');
            //enable buttons after finish loading
            $('.has-spinner').removeAttr("disabled");
        }
    }
})(jQuery);




$(document).ready(function(){
  // if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length || $('#editcontentForm').length)
  // {
  //   $('#state').trigger('change');
  // }

  toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-center",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }
  $("#signinForm").validate({
    rules: {
      mobile_number: {
        required: true,
        number: true,
        minlength: 10,
        maxlength: 10

      },
      password: {
        required: true,
      }
    },
    messages: {
      mobile_number: {
        required: "Please enter a mobile number",
        number: "Please enter valid mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits"

      },
      password: {
        required: "Please provide a password",
      }
    },
    errorPlacement: function(error, element) {
      error.appendTo(element.parent("div"));
    },
    submitHandler: function() {
        var btn = $('#submitBtn');
        $(btn).buttonLoader('start');
        $.ajax({
          'method':'POST',
          'url':'',
          'data': $('#signinForm').serialize(),
          success: function(response){
            if(response.status=='success')
            {
              $(btn).buttonLoader('stop')
              toastr.success('Login successfully.').delay(10000);
              window.location.href="roleselection";

            }
            else
            {
              $(btn).buttonLoader('stop')
              toastr.error(response.msg)
            }

          },
          error: function(xhr,status,errorThrown){
            toastr.error(xhr.responseText)
            $(btn).buttonLoader('stop')
          },
        });
      return false;
    }
  });


  $("#roleselectionForm").validate({
    rules: {
      roles: {
        required: true,
      }
    },
    messages: {
      roles: {
        required: "Please select a role",
      }
    },
    errorPlacement: function(error, element) {
      error.appendTo(element.parent("div"));
    },
    submitHandler: function() {
        var btn = $('#submitBtn');
        $(btn).buttonLoader('start');
        $.ajax({
          'method':'POST',
          'url':'',
          'data': $('#roleselectionForm').serialize(),
          success: function(response){
            if(response.status=='success')
            {
              $(btn).buttonLoader('stop')
              toastr.success('Login successfully.').delay(10000);
              window.location.href="/dashboard/";

            }
            else
            {
              $(btn).buttonLoader('stop')
              toastr.error(response.msg)
            }

          },
          error: function(xhr,status,errorThrown){
            toastr.error(xhr.responseText)
            $(btn).buttonLoader('stop')
          },
        });
      return false;
    }
  });

  $("#addschoolForm").validate({
    ignore: ":hidden",
    rules: {
      school_name: {
        required: true,

      },
      school_label: {
        required: true,
        remote: {
          url: "/school/check_school_lable",
          type: "post",
          data: {
            school_label: function() {
              return $( "#school_label" ).val();
            }
          }
        }
      },
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true,
        remote: {
          url: "/users/check_user_mobile",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
      },
      iml_school_code: {
        required: true,
      },
      country: {
        required: true,
      },
      state: {
        required: true,
      },
      city: {
        required: true,
      },
      board: {
        required: true,
      },
      medium: {
        required: true,
      },
      dise_no: {
        required: true,
      },
      class_label:{
        required: true,
      },
      disivion_label:{
        required: true,
      },
      module_manager:{
        required: true,
      },
      school_admin_name:{
        required: true,
      },
      school_admin_number:{
        required: true,
      }

    },
    messages: {
      school_name: {
        required: "Please enter a school name",
      },
      school_label: {
        required: "Please enter a school label",
        remote: "school label already exists"
      },
      iml_school_code: {
        required: "Please enter a Iml Code",
      },
      country: {
        required: "Please select a country",
      },
      state: {
        required: "Please select a state",
      },
      city: {
        required: "Please select a city",
      },
      board: {
        required: "Please select a board",
      },
      medium: {
        required: "Please select a medium",
      },
      dise_no: {
        required: "Please enter a Dise no",
      },
      class_label: {
        required: "Please enter a class label",
      },
      disivion_label: {
        required: "Please enter a division lable",
      },
      module_manager: {
        required: "Please select a module manager",
      },
      school_admin_name: {
        required: "Please enter a admin name",
      },
      school_admin_number: {
        required: "Please enter a admin number",
      },

      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('addschoolForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/school/add_school',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('School added successfully').delay(10000);
              setTimeout(function(){  window.location.href="/school/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

$("#editschoolForm").validate({

        ignore: ":hidden",
        rules: {
            school_name: {
                required: true,

            },
            school_label: {
                required: true,
                remote: {

                    url: "/school/check_edit_school_lable",
                    type: "post",
                    data: {

                school_id_pk: $('#school_id_pk').val(),

                        school_label: function () {
                            return $("#school_label").val();
                        }
                    }
                }
            },
            mobile_number: {
                required: true,
                minlength: 10,
                maxlength: 10,
                number: true,
                remote: {
                    url: "/users/check_user_mobile/",
                    type: "post",
                    data: {
                        mobile_number: function () {
                            return $("#mobile_number").val();
                        }
                    }
                }
            },
            iml_school_code: {
                required: true,
            },
            country: {
                required: true,
            },
            state: {
                required: true,
            },
            city: {
                required: true,
            },
            board: {
                required: true,
            },
            medium: {
                required: true,
            },
            dise_no: {
                required: true,
            },
            class_label: {
                required: true,
            },
            disivion_label: {
                required: true,
            },
            module_manager: {
                required: true,
            },
            school_admin_name: {
                required: true,
            },
            school_admin_number: {
                required: true,
            }

        },
        messages: {
            school_name: {
                required: "Please enter a school name",
            },
            school_label: {
                required: "Please enter a school label",
                remote: "school label already exists"
            },
            iml_school_code: {
                required: "Please enter a Iml Code",
            },
            country: {
                required: "Please select a country",
            },
            state: {
                required: "Please select a state",
            },
            city: {
                required: "Please select a city",
            },
            board: {
                required: "Please select a board",
            },
            medium: {
                required: "Please select a medium",
            },
            dise_no: {
                required: "Please enter a Dise no",
            },
            class_label: {
                required: "Please enter a class label",
            },
            disivion_label: {
                required: "Please enter a division lable",
            },
            module_manager: {
                required: "Please select a module manager",
            },
            school_admin_name: {
                required: "Please enter a admin name",
            },
            school_admin_number: {
                required: "Please enter a admin number",
            },

            mobile_number: {
                required: "Please enter a mobile number",
                minlength: "Your mobile number must consist of at least 10 digits",
                maxlength: "Your mobile number must consist of at max 10 digits",
                number: "Please enter valid mobile number",
                remote: "Mobile number already exists"
            }
        },
        submitHandler: function () {
            var userForm = document.getElementById('editschoolForm');
            var formData = new FormData(userForm);
            var user_id_pk = document.getElementById('user_id_pk').value;
            var school_id_pk = document.getElementById('school_id_pk').value;
            $.ajax({
                'method': 'POST',
                'url': '/school/edit_school/' + school_id_pk + '/' + user_id_pk,
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {
                        toastr.success('School added successfully').delay(10000);
                        setTimeout(function () {
                            window.location.href = "/school/";
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });

  $("#userForm").validate({
    ignore: ":hidden",
    rules: {
      user_type: {
        required: true,

      },
      name: {
        required: true,
      },
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true,

      },
      gender: {
        required: true,
      },
      email: {
        email: true,
      },
      password: {
        required: true,
      },
      re_password: {
        required: true,
      }
    },
    messages: {
      user_type: {
        required: "Please select a user type",
      },
      name: {
        required: "Please enter a name",
      },
      gender: {
        required: "Please select a gender",
      },
      password: {
        required: "Please enter a password",
      },
      re_password: {
        required: "Please enter a retype password",
      },
      email: {
        email: "Please enter valid email address",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number"
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('userForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/users/add_user',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('User added successfully').delay(10000);
              setTimeout(function(){  window.location.href="/users/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

  $("#edituserForm").validate({
    ignore: ":hidden",
    rules: {
      user_type: {
        required: true,

      },
      name: {
        required: true,
      },
      email: {
        email: true,
      },
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true,
        remote: {
          url: "/users/check_user_mobile",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            },
            user_id: function() {
              return $( "#user_id_pk" ).val();
            }
          }
        }
      },
      gender: {
        required: true,
      },
      email: {
        email: true,
      },
      password: {
        required: true,
      },
      re_password: {
        required: true,
      },
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      email: {
        email: "Please enter valid email address",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      },
      gender: {
        required: "Please select a gender",
      },
      password: {
        required: "Please enter a password",
      },
      re_password: {
        required: "Please enter a retype password",
      },
      email: {
        email: "Please enter valid email address",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('edituserForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/users/edit_user/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('User updated successfully').delay(10000);
              setTimeout(function(){ window.location.href="/users/"; }, 2000);

            }
            else
            {
              toastr.error(response.msg).delay(10000)

            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });



$("#roleForm").validate({
    ignore: ":hidden",
    rules: {

      name: {
        required: true,
      }
    },
    messages: {

      name: {
        required: "Please enter a role",
      },

    },
    submitHandler: function() {
      var userForm=document.getElementById('roleForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/roles/add_role',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('Role added successfully').delay(10000);
              setTimeout(function(){  window.location.href="/roles/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

  $("#editroleForm").validate({
    ignore: ":hidden",
    rules: {

      name: {
        required: true,
      }
    },
    messages: {

      name: {
        required: "Please enter a role",
      },

    },
    submitHandler: function() {
      var userForm=document.getElementById('editroleForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('role_id').value;
       console.log(user_id_pk);
        $.ajax({
          'method':'POST',
          'url':'/roles/save_role/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('Role updated successfully').delay(10000);
              setTimeout(function(){  window.location.href="/roles/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

  $("#mark_attd").validate({
    ignore: ":hidden",
    rules: {

      attd_date: {
        required: true,
      },

    },
    messages: {

      attd_date: {
        required: "Please select a date",
      },

    },
    submitHandler: function() {
      var userForm=document.getElementById('mark_attd');
      // console.log(userForm);
       var formData = new FormData(userForm);
       console.log(formData);
        $.ajax({
          'method':'POST',
          'url':'/attendance/save_attendance/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('Attendance updated successfully').delay(10000);
              setTimeout(function(){  window.location.href="/attendance/"; 
              return false;
              }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

 
  $("#view_attd").validate({
    ignore: ":hidden",
    rules: {

      start_date: {
        required: true,
      },
      end_date: {
        required: true,
      },
      class_list:{
        required:true,
      },
      division_list:{
        required:true,
      },
    },
    messages: {

      start_date: {
        required: "Please select start date",
      },
      end_date: {
        required: "Please select end date",
      },
      class_list: {
        required: "Please select a Class",
      },
      division_list: {
        required: "Please select a Division",
      },
      submitHandler: function() {
        var userForm=document.getElementById('view_attd');
         var formData = new FormData(userForm);
         console.log(userForm);
          $.ajax({
            'method':'POST',
            'url':'/attendance/',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              console.log(response);
              if (response.status == "error"){
                console.log('error');
                toastr.error(response.msg).delay(10000);
              }
              else if (response.status=="success")
              {
                // toastr.error(response.msg).delay(10000);
                setTimeout(function(){  window.location.href="/attendance/"; 
                return false;
                }, 2000);
              }
              else
              {
                toastr.error(response.msg).delay(10000);
              }
  
            },
            error: function(xhr,status,errorThrown){
              alert(xhr.responseText)
            },
          });
        return false;
      }
    }
  });  

 $("#addexamForm").validate({
        ignore: ":hidden",
        rules: {

            exam_name: {
                required: true,
            },
            description: {
                required: true,
            },
            country: {
                required: true,
            },
            state: {
                required: true
            },
            city: {
                required: true
            },
            class_master: {
                required: true
            },
            board: {
                required: true
            },
            medium: {
                required: true
            },
            school: {
                required: true,
            },
            amount: {
                required: true,
            },
            total_amount: {
                required: true,
            },
            exam_date: {
                required: true,
            },
            start_date: {
                required: true,
            },
            last_date: {
                required: true,
            }
        },
        messages: {

            exam_name: {
                required: "Please enter a exam",
            },
            description: {
                required: "Please enter a description",
            },
            country: {
                required: "Please select country",
            },
            school: {
                required: "Please select school",
            },
            state: {
                required: "Please select a state",
            },
            city: {
                required: "Please select a city",
            },
            board: {
                required: "Please select a board",
            },
            medium: {
                required: "Please select a medium",
            },
            class_master: {
                required: "Please select a class master",
            },
            amount: {
                required: "Please enter a exam amount",
            },
            total_amount: {
                required: "Please enter a exam total amount",
            },
            start_date: {
                required: "Please select a start date",
            },
            last_date: {
                required: "Please select a last date",
            },
            exam_date: {
                required: "Please select a exam date",
            },

        },
        submitHandler: function () {
            var userForm = document.getElementById('addexamForm');
            var formData = new FormData(userForm);
            $.ajax({
                'method': 'POST',
                'url': '/competitive_exam/add_competitive_exam',
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {

                        setTimeout(function () {
                            window.location.href = "/competitive_exam/post_competitive_exam/" + response.exam_id;
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });
    $("#editexamForm").validate({
        ignore: ":hidden",
        rules: {

            exam_name: {
                required: true,
            },
            description: {
                required: true,
            },
            country: {
                required: true,
            },
            state: {
                required: true
            },
            city: {
                required: true
            },
            class_master: {
                required: true
            },
            board: {
                required: true
            },
            medium: {
                required: true
            },
            school: {
                required: true,
            },
            amount: {
                required: true,
            },
            total_amount: {
                required: true,
            },
            exam_date: {
                required: true,
            },
            start_date: {
                required: true,
            },
            last_date: {
                required: true,
            }
        },
        messages: {

            exam_name: {
                required: "Please enter a exam",
            },
            description: {
                required: "Please enter a description",
            },
            country: {
                required: "Please select country",
            },
            school: {
                required: "Please select school",
            },
            state: {
                required: "Please select a state",
            },
            city: {
                required: "Please select a city",
            },
            board: {
                required: "Please select a board",
            },
            medium: {
                required: "Please select a medium",
            },
            class_master: {
                required: "Please select a class master",
            },
            amount: {
                required: "Please enter a exam amount",
            },
            total_amount: {
                required: "Please enter a exam total amount",
            },
            start_date: {
                required: "Please select a start date",
            },
            last_date: {
                required: "Please select a last date",
            },
            exam_date: {
                required: "Please select a exam date",
            },

        },
        submitHandler: function () {
            var userForm = document.getElementById('editexamForm');
            var formData = new FormData(userForm);
            var competitive_exam_id = $("#competitive_exam_id").val()
            $.ajax({
                'method': 'POST',
                'url': '/competitive_exam/edit_competitive_exam/'+competitive_exam_id,
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {

                        setTimeout(function () {
                            window.location.href = "/competitive_exam/post_competitive_exam/" + response.exam_id;
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });

    $("#sbt_confirm").click(function () {
        var exam_id = document.getElementById('exam_id').value;

        $.ajax({
            'method': 'POST',
            'url': '/competitive_exam/post_competitive_exam/' + exam_id,
            'dataType': 'json',
            success: function (response) {

                if (response.status == 'success') {

                    toastr.success('Exam created successfully').delay(10000);
                    setTimeout(function () {
                        window.location.href = "/competitive_exam/";
                    }, 2000);
                }
                else {
                    toastr.error(response.msg).delay(10000);
                }

            },
            error: function (xhr, status, errorThrown) {
                alert(xhr.responseText)
            },
        });
    });

    $("#sbt_cancel").click(function () {
        var exam_id = document.getElementById('exam_id').value;

        $.ajax({
            'method': 'POST',
            'url': '/competitive_exam/cancel_competitive_exam/' + exam_id,
            'dataType': 'json',
            success: function (response) {

                if (response.status == 'success') {

                    toastr.success('Exam canceled successfully').delay(10000);
                    setTimeout(function () {
                        window.location.href = "/competitive_exam/";
                    }, 2000);
                }
                else {
                    toastr.error(response.msg).delay(10000);
                }

            },
            error: function (xhr, status, errorThrown) {
                alert(xhr.responseText)
            },
        });
    });


 $("#moduleForm").validate({
    ignore: ":hidden",
    rules: {

      name: {
        required: true,
      },
      description: {
        required: true,
      },
      module_path: {
        required: true,
      }
    },
    messages: {

      name: {
        required: "Please enter a name",
      },
      description: {
        required: "Please enter a description",
      },
      module_path: {
        required: "Please enter a module path",
      }

    },
    submitHandler: function() {
      var userForm=document.getElementById('moduleForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/module_manager/add_module_manager',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('Module added successfully').delay(1000);
              setTimeout(function(){  window.location.href="/module_manager/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


 $("#editmoduleForm").validate({
    ignore: ":hidden",
    rules: {

      name: {
        required: true,
      },
      description: {
        required: true,
      },
      module_path: {
        required: true,
      }
    },
    messages: {

      name: {
        required: "Please enter a name",
      },
      description: {
        required: "Please enter a description",
      },
      module_path: {
        required: "Please enter a module path",
      }

    },
    submitHandler: function() {
      var userForm=document.getElementById('editmoduleForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/module_manager/edit_module_manager/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('Module updated successfully').delay(1000);
              setTimeout(function(){ window.location.href="/module_manager/"; }, 2000);

            }
            else
            {
              toastr.error(response.msg).delay(10000)

            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


   $("#uploadCSV").validate({
        rules: {
            file: {
                required: true,
                extension: "xlsx"

            }
        },
        file: {
            message: {
                required: "Please select a xlsx",
                extension: "Please upload a xlsx file",
            }
        },
        errorPlacement: function (error, element) {
            error.appendTo(element.parent("div"));
        },
        submitHandler: function () {
            var btn = $('#submitBtn');
            $(btn).buttonLoader('start');
            var userForm = document.getElementById('uploadCSV');
            var formData = new FormData(userForm);

            $.ajax({
                'method': 'POST',
                'url': '/school/add_school_excel/',
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {
                    if (response.status == 'success') {
                        $(btn).buttonLoader('stop')
                        toastr.success(response.msg).delay(10000);
                        setTimeout(function () {
                            window.location.href = "/school/";
                        }, 2000);

                    }
                    else {
                        $(btn).buttonLoader('stop')
                        toastr.error(response.msg)
                    }

                },
                error: function (xhr, status, errorThrown) {
                    toastr.error(xhr.responseText)
                    $(btn).buttonLoader('stop')
                },
            });
            return false;
        }
    });

 $("#adForm").validate({
    ignore: ":hidden",
    rules: {
      ad_name: {
        required: true,

      },
      message: {
        required: true,

      },
      contact_name: {
        required: true,

      },
      ad_url: {
        required: true,

      },
      ad_type: {
        required: true,

      },
      ad_position: {
        required: true,

      },
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true,
        remote: {
          url: "/users/check_user_mobile",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
      },
      country: {
        required: true,
      }

    },
    messages: {
      ad_name: {
        required: "Please enter a name",
      },
      message: {
        required: "Please enter a comment",
      },
      country: {
        required: "Please select a country",
      },
      ad_type: {
        required: "Please select Ad Type",
      },
      ad_position: {
        required: "Please select Ad Position",
      },
      ad_url: {
        required: "Please select a country",
      },

      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('adForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/advertisement/web_add',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('Advertisement added successfully').delay(10000);
              setTimeout(function(){  window.location.href="/advertisement/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

  $("#editadForm").validate({
    ignore: ":hidden",
    rules: {
      ad_name: {
        required: true,

      },
      message: {
        required: true,

      },
      contact_name: {
        required: true,

      },
      ad_url: {
        required: true,

      },
      ad_type: {
        required: true,

      },
      ad_position: {
        required: true,

      },
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true,
      },
      country: {
        required: true,
      }

    },
    messages: {
      ad_name: {
        required: "Please enter a name",
      },
      message: {
        required: "Please enter a comment",
      },
      country: {
        required: "Please select a country",
      },
      ad_type: {
        required: "Please select Ad Type",
      },
      ad_position: {
        required: "Please select Ad Position",
      },
      ad_url: {
        required: "Please select a country",
      },

      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('editadForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('save_ads').value;
       console.log(user_id_pk);
        $.ajax({
          'method':'POST',
          'url':'/advertisement/save_ads/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){

            if(response.status=='success')
            {
              toastr.success('Advertisement updated successfully').delay(1000);
              setTimeout(function(){ window.location.href="/advertisement/"; }, 2000);

            }
            else
            {
              toastr.error(response.msg).delay(10000)

            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


      $("#uploadCSVstudent").validate({
        rules: {
            file: {
                required: true,
                extension: "xlsx"

            }
        },
        file: {
            message: {
                required: "Please select a xlsx",
                extension: "Please upload a xlsx file",
            }
        },
        errorPlacement: function (error, element) {
            error.appendTo(element.parent("div"));
        },
        submitHandler: function () {
            var btn = $('#submitBtn');
            $(btn).buttonLoader('start');
            var userForm = document.getElementById('uploadCSVstudent');
            var formData = new FormData(userForm);

            $.ajax({
                'method': 'POST',
                'url': '/student/student_upload',
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {
                    if (response.status == 'success') {
                        $(btn).buttonLoader('stop')
                        toastr.success(response.msg).delay(10000);
                        setTimeout(function () {
                            window.location.href = "/student/";
                        }, 2000);

                    }
                    else {
                        $(btn).buttonLoader('stop')
                        toastr.error(response.msg)
                    }

                },
                error: function (xhr, status, errorThrown) {
                    toastr.error(xhr.responseText)
                    $(btn).buttonLoader('stop')
                },
            });
            return false;
        }
    });


    $("#editstudentForm").validate({
        ignore: ":hidden",
        rules: {
            student_first_name: {
                required: true,

            },
            roll_no: {
                required: true,
                /*remote: {
                 url: "/student/check_roll_no/"+$( "#roll_no" ).val()+'/'+$( "#class_label" ).val()+'/'+$( "#division_label" ).val()+'/'+$( "#student_id_pk" ).val(),
                 type: "post",
                 data: {
                 roll_no: function() {
                 return $( "#roll_no" ).val();
                 }
                 }
                 }*/
            },
            gr_no: {
                required: true,
                /*remote: {
                 url: "/student/check_gr_no/"+$( "#gr_no" ).val()+'/'+$( "#student_id_pk" ).val(),
                 type: "post",
                 data: {
                 gr_no: function() {
                 return $( "#gr_no" ).val();
                 }
                 }
                 }*/
            },
            // mobile_number: {
            //   required: true,
            //   minlength: 10,
            //   maxlength: 10,
            //   number: true,
            //   remote: {
            //     url: "/users/check_user_mobile/",
            //     type: "post",
            //     data: {
            //       mobile_number: function() {
            //         return $( "#mobile_number" ).val();
            //       }
            //     }
            //   }
            // },
            gender: {
                required: true,
            },
            country: {
                required: true,
            },
            state: {
                required: true,
            },
            city: {
                required: true,
            },
            dob: {
                required: true,
            },
            // roll_no: {
            //   required: true,
            // },
            // gr_no: {
            //   required: true,
            // },
            class_label: {
                required: true,
            },
            division_label: {
                required: true,
            },
            student_address: {
                required: true,
            },
            p_parent_first_name: {
                required: true,
            },
            p_parent_last_name: {
                required: true,
            },
            p_parent_email_id: {
                required: true,
            },
        },
        messages: {
            student_first_name: {
                required: "Please enter a student first name",
            },
            p_parent_first_name: {
                required: "Please enter a first name",

            },
            p_parent_last_name: {
                required: "Please enter a last name",
            },
            country: {
                required: "Please select a country",
            },
            state: {
                required: "Please select a state",
            },
            city: {
                required: "Please select a city",
            },
            roll_no: {
                required: "Please enter a roll no",
                remote: "Roll number already exists"
            },
            gr_no: {
                required: "Please enter a GR no",
                remote: "GR number already exists"
            },
            gender: {
                required: "Please select gender",
            },
            class_label: {
                required: "Please enter a class label",
            },
            division_label: {
                required: "Please enter a division lable",
            },
            dob: {
                required: "Please enter a date of birth",
            },
            p_parent_email_id: {
                required: "Please enter a email id",
            },
            student_address: {
                required: "Please enter a student address",
            },

            s_parent_mobile_no: {
                required: "Please enter a mobile number",
                minlength: "Your mobile number must consist of at least 10 digits",
                maxlength: "Your mobile number must consist of at max 10 digits",
                number: "Please enter valid mobile number",

            }
        },
        submitHandler: function () {
            var userForm = document.getElementById('editstudentForm');
            var formData = new FormData(userForm);
            var student_id_pk = document.getElementById('student_id_pk').value;
            $.ajax({
                'method': 'POST',
                'url': '/student/edit_student/' + student_id_pk,
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {
                        toastr.success('Student Details Updated successfully').delay(10000);
                        setTimeout(function () {
                            window.location.href = "/student/";
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });

    $("#resourceForm").validate({
        ignore: ":hidden",
        rules: {
            resource_name: {
                required: true
            },
            resource_description: {
                required: true
            },
            country: {
                required: true
            },
            state: {
                required: true
            },
            city: {
                required: true
            },
            school: {
                required: true
            },
            class_master: {
                required: true
            },
            board: {
                required: true
            },
            medium: {
                required: true
            },
            content_type: {
                required: true
            }

        },
        messages: {
            resource_name: {
                required: "Please enter a name"
            },
            resource_description: {
                required: "Please enter a description"
            },
            country: {
                required: "Please select a country"
            },
            state: {
                required: "Please select a state"
            },
            city: {
                required: "Please select a city"
            },
            school: {
                required: "Please select a school"
            },
            class_master: {
                required: "Please select a class"
            },
            board: {
                required: "Please select a board"
            },
            medium: {
                required: "Please select a medium"
            },
            content_type: {
                required: "Please select a content type"
            },
        },
        submitHandler: function () {
            var userForm = document.getElementById('resourceForm');
            var formData = new FormData(userForm);
            $.ajax({
                'method': 'POST',
                'url': '/resources/add',
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {
                        toastr.success('Resources added successfully').delay(10000);
                        setTimeout(function () {
                            window.location.href = "/resources/";
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });
    $("#editresource").validate({
        ignore: ":hidden",
        rules: {
            resource_name: {
                required: true
            },
            resource_description: {
                required: true
            },
            country: {
                required: true
            },
            state: {
                required: true
            },
            city: {
                required: true
            },
            school: {
                required: true
            },
            class_master: {
                required: true
            },
            board: {
                required: true
            },
            medium: {
                required: true
            },
            content_type: {
                required: true
            }

        },
        messages: {
            resource_name: {
                required: "Please enter a name"
            },
            resource_description: {
                required: "Please enter a description"
            },
            country: {
                required: "Please select a country"
            },
            state: {
                required: "Please select a state"
            },
            city: {
                required: "Please select a city"
            },
            school: {
                required: "Please select a school"
            },
            class_master: {
                required: "Please select a class"
            },
            board: {
                required: "Please select a board"
            },
            medium: {
                required: "Please select a medium"
            },
            content_type: {
                required: "Please select a content type"
            },
        },
        submitHandler: function () {
            var userForm = document.getElementById('editresource');
            console.log(userForm);
            var formData = new FormData(userForm);
            console.log(formData);
            // var base_url=window.location.href = "/resources/"
            var resource_id = document.getElementById('save_resource').value;
            console.log(resource_id);
            // var resource_url=base_url+'save_resources/' + resource_id
            // console.log(resource_url);
            $.ajax({
                'method': 'POST',
                'url':'/resources/save_resources/'+resource_id,
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {
                        toastr.success('Resource updated successfully').delay(1000);
                        setTimeout(function () {
                            window.location.href = "/resources/";
                        }, 2000);

                    }
                    else {
                        toastr.error(response.msg).delay(10000)

                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },

            });

            return false;
        }
    });


    $("#addfeesForm").validate({
        ignore: ":hidden",
        rules: {
            fees_title: {
                required: true,
            },
            fees_desc: {
                required: true,
            },
            fees_bank_name: {
                required: true,
            },


        },
        messages: {
            fees_title: {
                required: "Please enter a fees title",
            },
            fees_desc: {
                required: "Please enter a fees description",
            },

            fees_bank_name: {
                required: "Please select a bank",
            }

        },
        submitHandler: function () {
            var userForm = document.getElementById('addfeesForm');
            var formData = new FormData(userForm);
            $.ajax({
                'method': 'POST',
                'url': '/fees/add_fees',
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {
                        toastr.success('Fess added successfully').delay(10000);
                        setTimeout(function () {
                            window.location.href = "/fees/";
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });
    $("#editdivision").validate({
      ignore: ":hidden",
      rules: {
        division_name: {
          required: true,
          
        },
        division_description: {
          required: true,
          
        }
  
      },
      messages: {
        division_name: {
          required: "Please enter a name",
        },
        division_description: {
          required: "Please enter a description",
        }
      },
      submitHandler: function() {
        var userForm=document.getElementById('editdivision');
         var formData = new FormData(userForm);
         var user_id_pk=document.getElementById('save_div').value;
         console.log(user_id_pk);
          $.ajax({
            'method':'POST',
            'url':'/division/save_division/'+user_id_pk,
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
             
              if(response.status=='success')
              {
                toastr.success('Division updated successfully').delay(1000);
                setTimeout(function(){ window.location.href="/division/"; }, 2000);
                
              }
              else
              {
                toastr.error(response.msg).delay(10000)
                
              }
  
            },
            error: function(xhr,status,errorThrown){
              alert(xhr.responseText)
            },
          });
        return false;
      }
    });
  
    $("#editsubject").validate({
      ignore: ":hidden",
      rules: {
        subject_name: {
          required: true,
        },subject_status:{
          required:true,
        }
      },
      messages: {
        subject_name: {
          required: "Please enter a name",
        }
      },
      submitHandler: function() {
         var userForm=document.getElementById('editsubject');
         console.log(userForm);
         var formData = new FormData(userForm);
         console.log(formData);
         console.log("in javascript");
         var user_id_pk=document.getElementById('save_sub').value;
         console.log(user_id_pk);
          $.ajax({
            'method':'POST',
            'url':'/subject/save_subject/'+user_id_pk,
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
             
              if(response.status=='success')
              {
                toastr.success('Subject updated successfully').delay(1000);
                setTimeout(function(){ window.location.href="/subject/"; }, 2000);
                
              }
              else
              {
                toastr.error(response.msg).delay(10000)
                
              }
  
            },
            error: function(xhr,status,errorThrown){
              alert(xhr.responseText)
            },
          });
        return false;
      }
    });
    
    $("#editteacher").validate({
      ignore: ":hidden",
      rules: {
        teacher_name: {
          required: true,
          
        },
        teacher_mobile: {
          required: true,
        }
        ,
        teacher_email: {
          required: true,
        },
        teacher_dob: {
          required: true,
        }
        ,
        teacher_address: {
          required: true,
        }
      },
      messages: {
        teacher_name: {
          required: "Please enter a name",
        },
        teacher_mobile: {
          required: "Please enter a mobile number",
        },
        teacher_email: {
          required: "Please enter an email",
        },
        teacher_dob: {
          required: "Please enter a date of birth",
        },
        teacher_address: {
          required: "Please enter a address",
        }
      },
      submitHandler: function() {
        var userForm=document.getElementById('editteacher');
         var formData = new FormData(userForm);
         var user_id_pk=document.getElementById('save_teacher').value;
         console.log(user_id_pk);
         console.log(userForm);
          $.ajax({
            'method':'POST',
            'url':'/teacher/save_teacher/'+user_id_pk,
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
             
              if(response.status=='success')
              {
                toastr.success('Teacher updated successfully').delay(1000);
                setTimeout(function(){ window.location.href="/teacher/"; }, 2000);
                
              }
              else
              {
                toastr.error(response.msg).delay(10000)
                
              }
  
            },
            error: function(xhr,status,errorThrown){
              alert(xhr.responseText)
            },
          });
        return false;
      }
    });
  
  
  
  $("#upload_division").validate({
      rules: {
        file: {
          required: true,
          extension: "xlsx"
          
        }
      },
      file: {
        message: {
          required: "Please select a xlsx",
          extension: "Please upload a xlsx file",
        }
      },
      errorPlacement: function(error, element) {
        error.appendTo(element.parent("div"));
      },
      submitHandler: function() {
          var btn = $('#submitBtn');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('upload_division');
          var formData = new FormData(userForm);
          
          $.ajax({
            'method':'POST',
            'url':'/division/add',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.href="/division/"; }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });
  
    $("#upload_teacher").validate({
      rules: {
        file: {
          required: true,
          extension: "xlsx"
          
        }
      },
      file: {
        message: {
          required: "Please select a xlsx",
          extension: "Please upload a xlsx file",
        }
      },
      errorPlacement: function(error, element) {
        error.appendTo(element.parent("div"));
      },
      submitHandler: function() {
          var btn = $('#submitBtn');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('upload_teacher');
          var formData = new FormData(userForm);
          
          $.ajax({
            'method':'POST',
            'url':'/teacher/add',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              console.log(response);
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.assign("/teacher/"); }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });
  
  
  $("#upload_subject_teacher").validate({
      rules: {
        file: {
          required: true,
          extension: "xlsx"
          
        }
      },
      file: {
        message: {
          required: "Please select a xlsx",
          extension: "Please upload a xlsx file",
        }
      },
      errorPlacement: function(error, element) {
        error.appendTo(element.parent("div"));
      },
      submitHandler: function() {
          var btn = $('#submitBtn');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('upload_subject_teacher');
          var formData = new FormData(userForm);
          console.log(userForm);
          $.ajax({
            'method':'POST',
            'url':'/subject/subject_teacher',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.href="/subject/"; }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });
  
  
  
  $("#upload_subject").validate({
      rules: {
        file: {
          required: true,
          extension: "xlsx"
          
        }
      },
      file: {
        message: {
          required: "Please select a xlsx",
          extension: "Please upload a xlsx file",
        }
      },
      errorPlacement: function(error, element) {
        error.appendTo(element.parent("div"));
      },
      submitHandler: function() {
          var btn = $('#submitBtn');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('upload_subject');
          var formData = new FormData(userForm);
          
          $.ajax({
            'method':'POST',
            'url':'/subject/add',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.href="/subject/"; }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });
  
  $("#assignpermission").validate({
      ignore: ":hidden",
      rules: {
          users: {
              required: true,
          },
          app: {
              required: true,
          },
          content: {
              required: true,
          },
          permission: {
              required: true,
          }
      },
      messages: {
          users: {
              required: "Please select user",
          },
          app: {
              required: "Please select app",
          },

          content: {
              required: "Please enter content",
          },
          permission: {
              required: "Please select a permission",
          }

      },
      submitHandler: function() {
          var btn = $('#save_perms');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('assignpermission');
          var formData = new FormData(userForm);
          console.log(formData);
          $.ajax({
            'method':'POST',
            'url':'/permissions/user_permission',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.href="/permissions/"; }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });

    $("#assigngroups").validate({
      ignore: ":hidden",
      rules: {
          users: {
              required: true,
          },
          groups: {
              required: true,
          }
      },
      messages: {
          users: {
              required: "Please select user",
          },
          groups: {
              required: "Please select group",
          }

      },
      submitHandler: function() {
          var btn = $('#save_groups');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('assigngroups');
          var formData = new FormData(userForm);
          console.log(formData);
          $.ajax({
            'method':'POST',
            'url':'/permissions/user_group',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.href="/permissions/"; }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });
 
    
    $("#groupperms").validate({
      ignore: ":hidden",
      rules: {
          groups: {
              required: true,
          },
          app: {
              required: true,
          },
          content: {
              required: true,
          },
          permission: {
              required: true,
          }
      },
      messages: {
          groups: {
              required: "Please select group",
          },
          app: {
              required: "Please select app",
          },

          content: {
              required: "Please enter content",
          },
          permission: {
              required: "Please select a permission",
          }

      },
      submitHandler: function() {
          var btn = $('#save_groupperms');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('groupperms');
          var formData = new FormData(userForm);
          console.log(formData);
          $.ajax({
            'method':'POST',
            'url':'/permissions/group_permission',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.href="/permissions/"; }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });

  
  $("#upload_class_teacher").validate({
      rules: {
        file: {
          required: true,
          extension: "xlsx"
          
        }
      },
      file: {
        message: {
          required: "Please select a xlsx",
          extension: "Please upload a xlsx file",
        }
      },
      errorPlacement: function(error, element) {
        error.appendTo(element.parent("div"));
      },
      submitHandler: function() {
          var btn = $('#submitBtn');
          $(btn).buttonLoader('start');
          var userForm=document.getElementById('upload_class_teacher');
          var formData = new FormData(userForm);
          
          $.ajax({
            'method':'POST',
            'url':'/subject/class_teacher',
            'data': formData,
            'cache':false,
            'contentType': false,
            'processData': false,
            success: function(response){
              if(response.status=='success')
              {
                $(btn).buttonLoader('stop')
                toastr.success(response.msg).delay(10000);
                setTimeout(function(){ window.location.href="/teacher/"; }, 2000);  
  
              }
              else
              {
                $(btn).buttonLoader('stop')
                toastr.error(response.msg)
              }
  
            },
            error: function(xhr,status,errorThrown){
              toastr.error(xhr.responseText)
              $(btn).buttonLoader('stop')
            },
          });
        return false;
      }
    });
    $("#editfeesForm").validate({
        ignore: ":hidden",
        rules: {
            fees_title: {
                required: true,
            },
            fees_desc: {
                required: true,
            },
            fees_bank_name: {
                required: true,
            }

        },
        messages: {
            fees_title: {
                required: "Please enter a fees title",
            },
            fees_desc: {
                required: "Please enter a fees description",
            },

            fees_bank_name: {
                required: "Please select a bank",
            }

        },

        submitHandler: function () {
            var userForm = document.getElementById('editfeesForm');
            var formData = new FormData(userForm);
            var fees_id_pk = document.getElementById('fees_id_pk').value;
            //var school_id_pk=document.getElementById('school_id_pk').value;
            $.ajax({
                'method': 'POST',
                'url': '/fees/edit_fees/' + fees_id_pk,//+'/'+user_id_pk,
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {
                        toastr.success('Fess edited successfully').delay(10000);
                        setTimeout(function () {
                            window.location.href = "/fees/";
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });

    $("#addfeesstructForm").validate({
        ignore: ":hidden",
        rules: {
            fees_class_name: {
                required: true,
            },
            fees_division_name: {
                required: true,
            },
            fees_amt: {
                required: true,
            },
            due_date: {
                required: true,
            }


        },
        messages: {
            fees_class_name: {
                required: "Please select a class",
            },
            fees_division_name: {
                required: "Please select a division",
            },

            fees_amt: {
                required: "Please enter an amount",
            },
            due_date: {
                required: "Please select a due date",
            }

        },
        submitHandler: function () {
            var userForm = document.getElementById('addfeesstructForm');
            var formData = new FormData(userForm);
            $.ajax({
                'method': 'POST',
                'url': '/fees_report/add_fees_structure',
                'data': formData,
                'cache': false,
                'contentType': false,
                'processData': false,
                success: function (response) {

                    if (response.status == 'success') {
                        toastr.success('Fess added successfully').delay(10000);
                        setTimeout(function () {
                            window.location.href = "/fees_report/";
                        }, 2000);
                    }
                    else {
                        toastr.error(response.msg).delay(10000);
                    }

                },
                error: function (xhr, status, errorThrown) {
                    alert(xhr.responseText)
                },
            });
            return false;
        }
    });
  $(document).on('change','#fees_bank_name',function(){
    var bank_id=$("#fees_bank_name").val();
    console.log(bank_id)
    if(bank_id!=='')
    {
      $.ajax({
        'method':'POST',
        'url':'/fees/get_account_no',
        'data': {'bank_id':bank_id},
        success: function(response){
          console.log(response);
          if(response.status=='success')
          {
              $("#fees_account_no").val(response.account_no)
          }

        },
        error: function(xhr,status,errorThrown){
          toastr.error(xhr.responseText)
        },
      });
    }
  })


$(document).on('change','#country',function(){
    var country_id=$(this).val();
    var select_country='';

    if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length || $('#editcontentForm').length)
    {
      var select_country=$('#state_select').val();;
    }
    if(country_id!='')
    {
      $.ajax({
        'method':'POST',
        'url':'/state/get_state/',
        'data': {'country_id':JSON.stringify(country_id)},
        success: function(response){
          console.log(response);
          if(response.status=='success')
          {
            $('#state').prop('disabled',true);
            $('#state').html('');
            $.each(response.state_data, function (i, item) {
              if(select_country!='')
              {
                var selected=false;
                if(select_country==item.id)
                {
                  selected=true;
                }
                $('#state').append($('<option>', {
                    value: item.id,
                    text : item.name,
                    selected:selected
                }));
              }
              else
              {
                $('#state').append($('<option>', {
                    value: item.id,
                    text : item.name,
                    //selected:true
                }));
              }
               $('#state').multiselect('rebuild');
            });
            $('#state').prop('disabled',false);
          }

        },
        error: function(xhr,status,errorThrown){
          toastr.error(xhr.responseText)
        },
      });
    }
  });

$(document).on('change','#state',function(){
    var state_id=$(this).val();
    //console.log(state_id)
    var select_city='';

    if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length || $('#editcontentForm').length)
    {
      var select_city=$('#city_select').val();;
    }
    if(state_id!='')
    {
      $.ajax({
        'method':'POST',
        'url':'/city/get_city/',
        'data': {'state_id':JSON.stringify(state_id)},
        success: function(response){
          console.log(response);
          if(response.status=='success')
          {
            $('#city').prop('disabled',true);
            $('#city').html('');
            $.each(response.city_data, function (i, item) {
              if(select_city!='')
              {
                var selected=false;
                if(select_city==item.id)
                {
                  selected=true;
                }
                $('#city').append($('<option>', {
                    value: item.id,
                    text : item.name,
                    selected:selected
                }));
              }
              else
              {
                $('#city').append($('<option>', {
                    value: item.id,
                    text : item.name,
                    //selected:true
                }));
              }
                $('#city').multiselect('rebuild');
            });
            $('#city').prop('disabled',false);
          }

        },
        error: function(xhr,status,errorThrown){
          toastr.error(xhr.responseText)
        },
      });
    }
  });





$(document).on('change','#medium',function(){
    var medium=$(this).val();
    var city=$('#city').val();
    var board=$('#board').val();
    var state=$('#state').val();

    if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length || $('#editcontentForm').length)
    {
      var select_city=$('#city_select').val();
    }
    if(city!='')
    {

      $.ajax({
        'method':'POST',
        'url':'/competitive_exam/get_school_list',
        'data': {'medium':JSON.stringify(medium),'board':JSON.stringify(board),'city':JSON.stringify(city),'state':JSON.stringify(state)},
        success: function(response){
          console.log(response);
          if(response.status=='success')
          {
            $('#school').prop('disabled',true);
            $('#school').html('');
            $.each(response.school_data, function (i, item) {
              if(select_city!='')
              {
                var selected=false;
                if(select_city==item.id)
                {
                  selected=true;
                }
                $('#school').append($('<option>', {
                    value: item.id,
                    text : item.name,
                    //selected:selected
                }));
              }
              else
              {
                $('#school').append($('<option>', {
                    value: item.id,
                    text : item.name,
                    //selected:true
                }));
              }
                $('#school').multiselect('rebuild');
            });
            $('#school').prop('disabled',false);
          }

        },
        error: function(xhr,status,errorThrown){
          toastr.error(xhr.responseText)
        },
      });
    }


  });


// $(document).on('change','#school',function(){
//     var school_id=$(this).val();
//     var select_city='';

//     if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length || $('#editcontentForm').length)
//     {
//       var select_city=$('#city_select').val();
//     }
//     if(school_id!='')
//     {


//       $.ajax({
//         'method':'POST',
//         'url':'/class_master/get_class',
//         'data': {'school_id':JSON.stringify(school_id)},
//         success: function(response){
//           console.log(response);
//           if(response.status=='success')
//           {
//             $('#class_master').prop('disabled',true);
//             $('#class_master').html('');
//             $.each(response.class_data, function (i, item) {
//               if(select_city!='')
//               {
//                 var selected=false;
//                 if(select_city==item.id)
//                 {
//                   selected=true;
//                 }
//                 $('#class_master').append($('<option>', {
//                     value: item.id,
//                     text : item.name,
//                     //selected:selected
//                 }));
//               }
//               else
//               {
//                 $('#class_master').append($('<option>', {
//                     value: item.id,
//                     text : item.name,
//                     //selected:true
//                 }));
//               }
//                 $('#class_master').multiselect('rebuild');
//             });
//             $('#class_master').prop('disabled',false);
//           }

//         },
//         error: function(xhr,status,errorThrown){
//           toastr.error(xhr.responseText)
//         },
//       });
//     }
//   });

  function ResetForm() {
        document.getElementById("FORM1").reset();
        document.getElementById("Sample").innerHTML="Form has been reset";
     }

  $('#searchDate').daterangepicker({
    autoUpdateInput: false,
    locale: {
      format: 'DD/MM/YYYY'
    }
  });

  $('#searchDate').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
  });

  $('#searchDate').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });

  $('#reservationtime').daterangepicker({
    timePicker: true,
    timePicker24Hour:true,
    singleDatePicker:true,
    autoUpdateInput: false,
    locale: {
      format: 'DD/MM/YYYY HH:mm'
    }
  });
  $('#reservationtime').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('DD/MM/YYYY HH:mm'));
  });

  $('#reservationtime').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
  var summernoteElement = $('.ckeditor');
  var summernoteElementEdit = $('.ckeditoredit');
  summernoteElement.summernote({
    height: 200,
  });
  summernoteElementEdit.summernote({
    height: 200,
  });
});