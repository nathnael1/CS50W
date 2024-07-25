
    document.addEventListener('DOMContentLoaded', function() {
     
    
        //sends user to see a person profile
        document.querySelectorAll('.postuser').forEach(element => {
            element.addEventListener("click", (event) => {
                event.preventDefault();
                let username = element.innerHTML
                window.location.href = `profile_view/${username}`    
        });
    });
    //following site
    
    document.querySelector('#followingPage').addEventListener('click',(event)=>{
        event.preventDefault()
        window.location.href = `following`
    })

    //editing post
    document.querySelectorAll('.edit').forEach(function(button) {
        button.addEventListener('click', function() {
            let content = this.closest('.published').querySelector('.content').innerHTML;
            let post_id = button.dataset.postid
            console.log(post_id)
            this.closest('.published').querySelector('.content').style.display="none";
            this.closest('.published').querySelector('.time').style.display="none";
            this.closest('.published').querySelector('.like').style.display="none";
            this.closest('.published').querySelector('.edit').style.display="none";
            this.closest('.published').querySelector('.delete').style.display="none";
            
            text = document.createElement('textarea')
            save = document.createElement('button')
            save.innerHTML = 'Save'
            text.innerHTML = content
            this.closest('.published').append(text)
            this.closest('.published').append(save)
            save.addEventListener('click',()=>{
                content = text.value
                fetch('edit',{
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                post_id: post_id,
                                content: content,
                                
                            })
                        })
                            .then(response => response.json())
                            .then(result => {
                                console.log(result.message)
                               text.style.display="none";
                                 save.style.display="none";

                                this.closest('.published').querySelector('.content').style.display="block";
                                this.closest('.published').querySelector('.time').style.display="block";
                                this.closest('.published').querySelector('.like').style.display="block";
                                this.closest('.published').querySelector('.edit').style.display="block";
                                this.closest('.published').querySelector('.delete').style.display="block";
                                this.closest('.published').querySelector('.content').innerHTML = content
                })
                            .catch(error => console.log('error', error))
                
            })
        });
    });
    // document.querySelector("#edit").addEventListener('click',()=>{
    //     post_id = document.querySelector("#edit").dataset.post_id
    //    
    // })

    // Getting the original value of number of follower 
    let value = document.querySelector("#followers").innerHTML;
    let number = '';
    for (let i = 0; i < value.length; i++) {
        if (!isNaN(Number(value[i]))) {
            number += value[i];
        }
    }
    let numberoriginal = parseInt(number, 10);




    //follow and unfollow function
    let followb = true
    let followbutton = document.querySelector("#follow")
    let unfollowbutton = document.querySelector("#unfollow")
    function follow(user){
        if (followb){
            followbutton = document.querySelector("#follow")
            fetch(`/follow/${user}`, {
                method: 'PUT'
            })
            .then(response => response.json())
            .then(result => {

                //increment follower by 1
                let value = document.querySelector("#followers").innerHTML;
                let number = '';
                for (let i = 0; i < value.length; i++) {
                    if (!isNaN(Number(value[i]))) {
                        number += value[i];
                    }
                }
                number = parseInt(number, 10);
                if (number <= numberoriginal){
                    number++
                    document.querySelector('#followers').innerHTML = `Followers: ${number}`
                }else{
                    document.querySelector('#followers').innerHTML = `Followers: ${number}`
                }
                


                document.querySelector('#follow').innerHTML = 'Unfollow'
                document.querySelector('#follow').id = 'unfollow'
                unfollowbutton = document.querySelector("#unfollow")
                unfollowbutton.disabled = false;
                document.querySelector("#unfollow").addEventListener('click',()=>{
                    document.querySelector('#unfollow').dataset.user = user
                    followb= false
                    follow(user)
                })
                
                
            })
            .catch(error => console.log('error', error)
        )
        }else{

            fetch(`/unfollow/${user}`, {
                method: 'PUT'
            })
            .then(response => response.json())
            .then(result => {


                //decrement follower number by 1 
                let value = document.querySelector("#followers").innerHTML;
                let number = '';
                for (let i = 0; i < value.length; i++) {
                    if (!isNaN(Number(value[i]))) {
                        number += value[i];
                    }
                }
                number = parseInt(number, 10);
                if (number >= numberoriginal){
                    number--
                    document.querySelector('#followers').innerHTML = `Followers: ${number}`
                }else{
                    document.querySelector('#followers').innerHTML = `Followers: ${number}`
                }



                document.querySelector('#unfollow').innerHTML = 'Follow'
                document.querySelector('#unfollow').id = 'follow'
                followbutton = document.querySelector("#follow")
                followbutton.disabled = false;
                document.querySelector("#follow").addEventListener('click',()=>{
                document.querySelector('#follow').dataset.user = user
                followb = true
                follow(user)
            })
                

            })
            .catch(error => console.log('error', error)
        )
        }

    }



    // to follow and unfollow
    if (followbutton){
        document.querySelector('#follow').addEventListener('click', () => {
            followb = true
            user = document.querySelector('#follow').dataset.user
            document.querySelector('#follow').disabled = true
            follow(user)
            
    
        })
    }
    if(unfollowbutton){
        document.querySelector('#unfollow').addEventListener('click', () => {
            user = document.querySelector('#unfollow').dataset.user
            document.querySelector('#unfollow').disabled = true
            followb = false
            follow(user)
    
        })
    }




    })
