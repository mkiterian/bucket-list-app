$(document).ready(function(){
  });

  $(".button-collapse").sideNav();

  $("#btn_add_activity").click(function(){
    $("#frm_add_activity").toggle(); 
  });

  $(".btn_update_bckt").click(function(){
    $("#frm_update_bckt_lst").toggle(); 
  });

  $("#btn_add_bckt").click(function(){
    $("#frm_add_bckt_lst").toggle(); 
  });
 
 
  $(document).ready(function(){
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
  });
          