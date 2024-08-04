document.addEventListener("DOMContentLoaded", function() {

// animation for the quote
    let quote = document.querySelector("#quote");
    let quotecontent = document.querySelector("#quotecontent");

    let random = Math.floor(Math.random() * 10);
    previous = random;
    let quotes = [
        "The only bad workout is the one that didn't happen.",
        "The body achieves what the mind believes.",
        "You are stronger than you think.",
        "Don't wish for it, work for it.",
        "Your only limit is you.",
        "The pain you feel today will be the strength you feel tomorrow.",
        "Don't count the days, make the days count.",
        "Strive for progress, not perfection.",
        "Push yourself because no one else is going to do it for you.",
        "The only way to finish is to start."
    ]
    quotecontent.innerHTML = `"${quotes[random]}"`;
    random = Math.floor(Math.random() * 10);
    while(random == previous)
    {
        random = Math.floor(Math.random() * 10);
    }
    previous = random;
    setInterval(function() {
        quotecontent.innerHTML = `"${quotes[random]}"`;
        quotecontent.classList.add("fadein");
        setTimeout(function() {
            quotecontent.classList.remove("fadein");
        }, 2000);
        random = Math.floor(Math.random() * 10);
        while(random == previous)
        {
            random = Math.floor(Math.random() * 10);
        }
        previous = random;
    }, 5000);


 // end tag for DOMContentLoaded   
})

