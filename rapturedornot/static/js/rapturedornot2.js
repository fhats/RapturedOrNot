//Facebook crap

FB.Event.subscribe('auth.login', function(response){
    alert(response.status);
    if( response.status == "notConnected" || response.status == "unknown" ){
        alert("Not logged in!!");
        return false;
    }
    else{
        //We got teh FBcksz!
        $.ajax({
            type: 'POST',
            url: '/login',
            data: {
                    fb_id: response.session.uid
                  },
            dataType: "json",
			success: function(data){
				if(data.status == "error" && data.needs == "friends"){
                    alert("need f!");
					FB.api('/me/friends', function(friendResponse) {
						//alert(JSON.stringify(friendResponse));
                        $.ajax({
                        	type: 'POST',
							url: '/create',
							data: {
								fb_id: response.session.uid,
								friendJson: JSON.stringify(friendResponse)
							},
                        });
					});
				}
				else if(data.status == "ok"){
					var requestURL = "/";
					requestURL.append(data.friendUID);
					requestURL.append("/picture");
					FB.api(requestURL,{type: "large"}, function(response){
						alert(JSON.stringify(response));
					});
				}
				else{
					alert("miss1!");
				}		
			},
            error: function(){
                alert("miss2!");
            }
        });

        $("#fb_info").empty();
        $("#fb_info").append("Hey you'z logged in!");
    }
});

function newFriendCallback(data){
    alert("fbcb!");
    if(data.status == "ok"){
        populateFriendArea(data.id, data.name);
    }
    else{
        alert("miss4!");
    }
}

function populateFriendArea(id, name){
    alert("popf!");
    $("#fb_content").empty();

    var requestURL = "/";
    requestURL.append(id);
    requestURL.append("/picture");
    FB.api(requestURL,{type: "large"}, function(response){
        alert(response);
    });
}