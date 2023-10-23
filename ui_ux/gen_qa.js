messages = [
    "Hey Alex, how's it going?",
    "Hey Sarah! I'm doing pretty well, thanks. How about you?",
    "Not bad, not bad. I finally finished that book you recommended. It was amazing!",
    "Oh, I'm glad you liked it! Isn't the plot just mind-blowing? What are you thinking of reading next?",
    "I'm thinking of diving into some classic literature. Maybe something by Jane Austen or Charles Dickens. Any suggestions?",
    'Oh, those are great choices! If you\'re up for some romance, go for "Pride and Prejudice." If you want something more on the dramatic side, try "Great Expectations."',
    "I think I'll start with \"Pride and Prejudice.\" Thanks! So, how's work treating you?",
    "It's been a bit hectic, to be honest. We have a big project deadline coming up, but I'm learning a lot in the process. How about you? How's your new job?",
    "It's been fantastic! The team is super supportive, and I'm getting to work on some really interesting projects. Plus, the office is right next to this amazing coffee shop.",
    "That sounds like the dream! What's your go-to coffee order?",
    "You know me, a classic cappuccino never disappoints. What about you? Are you still sticking to black coffee?",
    "Haha, you know it. I like to keep it simple. Hey, have you heard about that new art exhibit downtown? I heard it's supposed to be incredible.",
    "Yeah, I've been meaning to check it out. Let's make a plan to go this weekend.",
    "Sounds like a plan! I'm always up for some cultural enrichment.",
    "Perfect! I'll check the timings and let you know. Anything else exciting happening in your world?",
    "Well, I've been thinking about taking up a new hobby. Maybe photography or hiking. I need to get out more, you know?",
    "That's a great idea! Both options sound amazing. Let me know when you decide, maybe we can go for a hike together.",
    "Absolutely! It would be awesome to have some company. Alright, let's catch up soon, okay?",
    "Definitely! Talk to you soon, Alex.",
    "Take care, Sarah!",
];

messages.forEach((msg, i) => {
    if (i % 2 == 0) {
        $(".chat-window").append(
            $("<div>").attr("class", "user-chat").text(msg)
        );
    } else {
        $(".chat-window").append(
            $("<div>").attr("class", "system-chat").text(msg)
        );
    }
});
