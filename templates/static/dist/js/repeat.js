$(document).ready(function(){  
      var i=1;  
      $('#add').click(function(){  
           i++;  
           $('#dynamic_field').append('<tr id="row'+i+'"><td><input type="text" name="name[]" placeholder="Enter your Key" class="form-control name_list" /></td>><td><input type="text" name="name[]" placeholder="Enter your Velue" class="form-control name_list" /></td><td><button type="button" name="remove" id="'+i+'" class="btn btn-danger btn_remove">X</button></td></tr>');  
      });  
      $(document).on('click', '.btn_remove', function(){  
           var button_id = $(this).attr("id");   
           $('#row'+button_id+'').remove();  
      });  
      $('#submit').click(function(){            
           $.ajax({  
                url:"addmore.php",  
                method:"POST",  
                data:$('.add_name').serialize(),  
                success:function(data)  
                {  
                     alert(data);  
                     //$('#add_name')[0].reset();  
                }  
           });  
      }); 

      $('#add1').click(function(){  
           i++;  
           $('#dynamic_field1').append('<div id="row'+i+'" class="row" ><div class="col-lg-4"><div class="form-group"><label>Bank Name </label><input type="text" class="form-control" name="bank_name[]" id="bank_name" placeholder="Bank Name"></div></div><div class="col-lg-4"><div class="form-group"> <label>Account No</label> <input type="text" class="form-control" name="account_no[]" id="account_no" placeholder="Account No"> </div> </div> <div class="col-lg-4"> <div class="form-group"> <label>&nbsp;</label> </div> </div> <div class="col-lg-4"> <div class="form-group"> <label>IFSC Code </label> <input type="text" class="form-control" name="ifsc_code[]" id="ifsc_code" placeholder="IFSC Code"> </div> </div> <div class="col-lg-4"> <div class="form-group"> <label>Branch Name</label> <input type="text" class="form-control" name="branch_name[]" id="branch_name" placeholder="Branch Name"> </div> </div> <div class="col-lg-4"> <div class="form-group"> <label>&nbsp;</label><br/><button type="button" name="remove" id="'+i+'" class="btn btn-danger btn_remove">X</button> </div> </div> </div>');  
      });  
      $(document).on('click', '.btn_remove', function(){  
           var button_id = $(this).attr("id");   
           $('#row'+button_id+'').remove();  
      });  
      $('#submit').click(function(){            
           $.ajax({  
                url:"addmore.php",  
                method:"POST",  
                data:$('.add_name').serialize(),  
                success:function(data)  
                {  
                     alert(data);  
                     //$('#add_name')[0].reset();  
                }  
           });  
      });  
 }); 