$(document).ready(function(){
    $('.post_content_text').hide();
    $('.update_btn').hide();
    $('.cancel_btn').hide();
    $('.editBtn').on('click',function(){
        var post_id = $(this).data('post_id');
        $('.cancel_btn_'+post_id).fadeIn();
        $('.edit_btn_'+post_id).hide();
        $('.update_btn_'+post_id).fadeIn();
        var post_content = $('.post_content_p_'+post_id).text();
        $('.post_content_text_'+post_id).val(post_content);
        $('.post_content_text_'+post_id).fadeIn();
    });
    $('.cancel_btn').on('click',function(){
        var post_id = $(this).data('post_id');
        $('.update_btn_'+post_id).hide();
        $('.post_content_text_'+post_id).hide();
        $('.cancel_btn').hide();
        $('.editBtn').fadeIn();
    });
    
});

function submit(id,postLikes){
    const btn = document.getElementById(`${id}`);
    if(postLikes == 'unlike'){
        fetch(`/like/${id}`)
        .then(Response => Response.json)
        .then(result => {
            btn.style.color = "red"
            window.location.reload()
        }
    )} else{
        fetch(`/unlike/${id}`)
        .then(Response => Response.json)
        .then(result => {
            btn.style.color = "grey"
            window.location.reload()
        })
    }
}