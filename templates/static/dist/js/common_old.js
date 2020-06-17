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

$(document).on('change','#user_type',function(){
    var user=$(this).val();
    if(user=='3')
    {
      $('#show_farmer').show();
      $('.show_retailer_wholersaler').hide()
    }
    else
    {
      $('#show_farmer').hide();
      $('.show_retailer_wholersaler').show()
    }
  });
  $(document).on('change','.custom-file-input',function(){
    var img=$(this).val();
    $(this).next('.custom-file-label').html(img);
  });
  $(document).on('change','#state',function(){
    var state_id=$(this).val();
    var select_state='';
   
    if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length || $('#editcontentForm').length)
    {
      var select_state=$('#district_selct').val();;
    }
    if(state_id!='')
    {
      $.ajax({
        'method':'POST',
        'url':'/get_district/',
        'data': {'state_id':state_id},
        success: function(response){
          console.log(response);
          if(response.status=='success')
          {
            $('#district').prop('disabled',true);
            $('#district').html('<option  value="" selected="selected">---select---</option>');
            $.each(response.district_data, function (i, item) {
              if(select_state!='')
              {
                var selected=false;
                if(select_state==item.id)
                {
                  selected=true;
                }
                $('#district').append($('<option>', { 
                    value: item.id,
                    text : item.name,
                    selected:selected
                }));
              }
              else
              {
                $('#district').append($('<option>', { 
                    value: item.id,
                    text : item.name,
                    //selected:true
                }));
              }
                
            });
            $('#district').prop('disabled',false);
          }

        },
        error: function(xhr,status,errorThrown){
          toastr.error(xhr.responseText)
        },
      });
    }
  });

$(document).ready(function(){
  if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length || $('#editcontentForm').length)
  {
    $('#state').trigger('change');
  }
  
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
          'url':'/user_login/',
          'data': $('#signinForm').serialize(),
          success: function(response){
            if(response.status=='success')
            {
              $(btn).buttonLoader('stop')
              toastr.success('Login successfully.')
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
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
      },
      email: {
        email: true,
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
        remote: {
          url: "/check_aadhar_card/",
          type: "post",
          data: {
            aadhar_no: function() {
              return $( "#aadhar_no" ).val();
            }
          }
        }
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      },
      soil_card: {
        required: true,
      },
      land_area: {
        required: true,
	number: true,
      }
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
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
        remote: "Aadhar card no already exists"
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      },
      soil_card: {
        required: "Please select a image",
      },
      land_area: {
        required: "Please enter a land area",
	number: "Please enter valid number",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('userForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_user/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            
            if(response.status=='success')
            {
              toastr.success('User added successfully').delay(10000);
              setTimeout(function(){  window.location.href="/get_user/"; }, 2000);
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
          url: "/check_user_mobile/",
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
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
        remote: {
          url: "/check_aadhar_card/",
          type: "post",
          data: {
            aadhar_no: function() {
              return $( "#aadhar_no" ).val();
            },
            user_id: function() {
              return $( "#user_id_pk" ).val();
            }
          }
        }
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      }
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
      aadhar_no: {
        required: "Please enter a aadhar no",
        minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
        remote: "Aadhar card no already exists"
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('edituserForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_user/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
           
            if(response.status=='success')
            {
              toastr.success('User updated successfully').delay(10000);
              setTimeout(function(){ window.location.href="/get_user/"; }, 2000);
              
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


    $("#retailerForm").validate({
   
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
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      }
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('retailerForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_retailer/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
          
            if(response.status=='success')
            {
              toastr.success('Retailler added successfully').delay(10000);
              
              setTimeout(function(){ window.location.href="/get_retailer/"; }, 2000);
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


    $("#editretailerForm").validate({
   
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
        number: true
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      }
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('editretailerForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_retailer/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Retailler updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_retailer/"; }, 2000);
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

   
   $("#productForm").validate({
    rules: {
      product_name: {
        required: true,
        
      },
      product_price: {
        required: true,
        number: true
      }
    },
    messages: {
      product_name: {
        required: "Please enter a name",
      },
      product_price: {
        required: "Please enter a price",
        number: "Please enter valid price"
      }
    },

    submitHandler: function() {
       var productForm=document.getElementById('productForm');
       var formData = new FormData(productForm);
        $.ajax({
          'method':'POST',
          'url':'/add_product/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
           success: function(response){
            if(response.status=='success')
            {
              toastr.success('Product Add successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_product/"; }, 2000);
              
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

   $("#editproductForm").validate({
    rules: {
      product_name: {
        required: true,
        
      },
      product_price: {
        required: true,
        number: true
      }
    },
    messages: {
      product_name: {
        required: "Please enter a name",
      },
      product_price: {
        required: "Please enter a price",
        number: "Please enter valid price"
      }
    },

    submitHandler: function() {
       var productForm=document.getElementById('editproductForm');
       var formData = new FormData(productForm);
       var product_id=$('#product_id').val();
        $.ajax({
          'method':'POST',
          'url':'/edit_product/'+product_id,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
           success: function(response){
            if(response.status=='success')
            {
              toastr.success('Product updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_product/"; }, 2000);
            }
            else
            {
              toastr.error('Something went wrong.').delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


   $("#farmerForm").validate({
   
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
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      },
      soil_card: {
        required: true,
      },
      land_area: {
        required: true,
	number: true,
      }
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      },
      soil_card: {
        required: "Please select a image",
      },
      land_area: {
        required: "Please enter a land area",
	number: "Please enter valid number",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('farmerForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_farmer/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Farmer added successfully').delay(10000);
              setTimeout(function(){ window.location.href="/get_farmer/"; }, 2000);
              
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


    $("#editfarmerForm").validate({
   
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
        number: true
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      }
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('editfarmerForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_farmer/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Farmer updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_farmer/"; }, 2000);
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

$("#wholesalerForm").validate({
   
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
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      },
      soil_card: {
        required: true,
      },
      land_area: {
        required: true,
	number: "Please enter valid mobile number",
      }
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      },
      soil_card: {
        required: "Please select a image",
      },
      land_area: {
        required: "Please enter land area",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('wholesalerForm');
       var formData = new FormData(userForm);
      
        $.ajax({
          'method':'POST',
          'url':'/add_wholesaler/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Wholesaler added successfully').delay(10000);
              setTimeout(function(){ window.location.href="/get_wholesaler/"; }, 2000);
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


$("#editwholeselerForm").validate({
   
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
        number: true
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      }
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('editwholeselerForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_wholesaler/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Wholesaler updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_wholesaler/"; }, 2000);
              
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


$("#editloyalityForm").validate({
   
    rules: {
      loyalty_type: {
        required: true,
        
      },
      loyalty_point: {
        required: true,
      }
    },
    messages: {
      loyalty_type: {
        required: "Please enter a loyalty type",
      },
      loyalty_point: {
        required: "Please enter a loyalty point",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('editloyalityForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_loyalty/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('loyalty updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/loyalty_configuration/"; }, 2000);
              
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


/*
$("#dashboardForm").validate({
    rules: {
      searchDate: {
        required: true,
        
      }
    },
    messages: {
      searchDate: {
        required: "Please enter a date",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('dashboardForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/dashboard/'
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Wholesaler updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_wholesaler/"; }, 2000);
              
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });
*/


  var summernoteValidator = $("#contentForm").validate({
    errorElement: "div",
    errorClass: 'is-invalid',
    validClass: 'is-valid',
    ignore: ':hidden:not(.ckeditor),.note-editable.card-block',
    errorPlacement: function (error, element) {
        // Add the `help-block` class to the error element
        error.addClass("invalid-feedback");
        console.log(element);
        if (element.prop("type") === "checkbox") {
            error.insertAfter(element.siblings("label"));
        } else if (element.hasClass("ckeditor")) {
            error.insertAfter(element.siblings(".note-editor"));
        } else {
            error.insertAfter(element);
        }
    },
    rules:{
      title_eng: {
        required: true,
      },
      title_hnd: {
        required: true,
      },
      datetime:{
        required: true,
      },
      'user_type[]':
      {
        required:true,
      },   
      content_eng: {
        required: true,
      },
      content_hnd: {
        required: true,
      }            
    },
    submitHandler: function() {
      var userForm=document.getElementById('contentForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_content/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Content added successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_content/"; }, 2000);
              
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


  var summernoteValidatorEdit = $("#editcontentForm").validate({
    errorElement: "div",
    errorClass: 'is-invalid',
    validClass: 'is-valid',
    ignore: ':hidden:not(.ckeditor),.note-editable.card-block',
    errorPlacement: function (error, element) {
        // Add the `help-block` class to the error element
        error.addClass("invalid-feedback");
        console.log(element);
        if (element.prop("type") === "checkbox") {
            error.insertAfter(element.siblings("label"));
        } else if (element.hasClass("ckeditor")) {
            error.insertAfter(element.siblings(".note-editor"));
        } else {
            error.insertAfter(element);
        }
    },
    rules:{
      title_eng: {
        required: true,
      },
      title_hnd: {
        required: true,
      },
      datetime:{
        required: true,
      },
      'user_type[]':
      {
        required:true,
      },   
      content_eng: {
        required: true,
      },
      content_hnd: {
        required: true,
      }            
    },
    submitHandler: function() {
      var userForm=document.getElementById('editcontentForm');
       var formData = new FormData(userForm);
       var content_id=document.getElementById('content_id').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_content/'+content_id,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Content updated successfully.').delay(10000);
             setTimeout(function(){ window.location.href="/get_content/"; }, 2000);
              
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

  $("#supportChat").validate({
    rules: {
      message: {
        required: true,
        
      }
    },
    messages: {
      message: {
        required: "Please enter a message",
      }
    },
    errorPlacement: function(error, element) {
      error.appendTo(element.parent("div"));
    },
    submitHandler: function() {
        var btn = $('#submitBtn');
        var support_id=document.getElementById('support_id').value;
        $(btn).buttonLoader('start');
        $.ajax({
          'method':'POST',
          'url':'/view_support/'+support_id,
          'data': $('#supportChat').serialize(),
          success: function(response){
            if(response.status=='success')
            {
              $(btn).buttonLoader('stop')
              //toastr.success('Content updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/view_support/"+support_id; }, 1000);

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

  $("#uploadCSV").validate({
    rules: {
      file: {
        required: true,
        extension: "csv"
        
      }
    },
    file: {
      message: {
        required: "Please select a csv",
        extension: "Please select only csv file"
      }
    },
    errorPlacement: function(error, element) {
      error.appendTo(element.parent("div"));
    },
    submitHandler: function() {
        var btn = $('#submitBtn');
        $(btn).buttonLoader('start');
        var userForm=document.getElementById('uploadCSV');
        var formData = new FormData(userForm);
      
        $.ajax({
          'method':'POST',
          'url':'/add_wholesaler/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              $(btn).buttonLoader('stop')
              if(response.Number_Already_Exits>0)
              {
                toastr.success(response.Number_Already_Exits+' user(s) added successfully').delay(10000);  
              }
              if(response.Number_Of_User_Added>0)
              {
                toastr.success(response.Number_Already_Exits+' users alredy exist').delay(10000);  
              }
              //setTimeout(function(){ window.location.href="/add_wholesaler/"; }, 1000);

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

  var summernoteValidator = $("#notificationForm").validate({
    rules:{
      title_eng: {
        required: true,
      },
      title_hnd: {
        required: true,
      },
      'request_for[]':{
        required: true,
      },
      'user_type[]':
      {
        required:true,
      },   
      message_eng: {
        required: true,
      },
      message_hnd: {
        required: true,
      }            
    },
    errorElement: "div",
    errorClass: 'is-invalid',
    validClass: 'is-valid',
    errorPlacement: function (error, element) {
        // Add the `help-block` class to the error element
        error.addClass("invalid-feedback");
        console.log(element);
        if (element.prop("type") === "checkbox") {
            error.insertAfter(element.siblings("label"));
        } else if (element.hasClass("ckeditor")) {
            error.insertAfter(element.siblings(".note-editor"));
        } else {
            error.insertAfter(element);
        }
    },
    submitHandler: function() {
      var userForm=document.getElementById('notificationForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_notifications/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Notifications sent successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_notifications/"; }, 2000);
              
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

  $('.typeahead').typeahead(
  {  
      source: function(query, result)
      {
        $.ajax({
        url:"/search_city/",
        method:"GET",
        data:{query:query},
        //dataType:"json",
        success:function(data)
        {
          result($.map(data, function(item){
          return item;
          }));
        }
        })
      }
  });

  $('#product_unit_name').typeahead(
    {  
        source: function(query, result)
        {
          $.ajax({
          url:"/product_unit/",
          method:"GET",
          data:{query:query},
          //dataType:"json",
          success:function(data)
          {
            result($.map(data, function(item){
            return item;
            }));
          }
          })
        }
    });



  $('#searchDate').daterangepicker({
    locale: {
      format: 'DD/MM/YYYY'
    }
  });

  $('#reservationtime').daterangepicker({
    timePicker: true,
    timePicker24Hour:true,
    singleDatePicker:true,
    locale: {
      format: 'DD/MM/YYYY HH:mm'
    }
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
