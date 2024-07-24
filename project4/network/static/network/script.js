
    document.addEventListener('DOMContentLoaded', function() {
        // Ensure the URL is correctly rendered
    

        document.querySelectorAll('.postuser').forEach(element => {
            element.addEventListener("click", (event) => {
                event.preventDefault();
                let username = element.innerHTML
                window.location.href = `profile_view/${username}`    
        });
    });
    let value = document.querySelector("#followers").innerHTML;
    let number = '';
    for (let i = 0; i < value.length; i++) {
        if (!isNaN(Number(value[i]))) {
            number += value[i];
        }
    }
    let numberoriginal = parseInt(number, 10);
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
    if(unfollowbutton){
        document.querySelector('#unfollow').addEventListener('click', () => {
            user = document.querySelector('#unfollow').dataset.user
            document.querySelector('#unfollow').disabled = true
            followb = false
            follow(user)
    
        })
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



    })
