// =========================================================
// AI AGENT CHAT
// =========================================================

async function sendChatMessage() {

    const messageInput =
        document.getElementById("messageInput");

    const chatMessages =
        document.getElementById("chatMessages");

    const selectedAgent =
        document.getElementById("agentSelect");


    if (!messageInput || !chatMessages) {

        console.error(
            "Chat elements not found."
        );

        return;

    }


    const message =
        messageInput.value.trim();


    if (!message) {

        return;

    }


    // -----------------------------------------------------
    // GET SELECTED AGENT
    // -----------------------------------------------------

    let agentType = "secure";


    if (selectedAgent) {

        agentType =
            selectedAgent.value;

    }


    console.log(
        "SELECTED AGENT:",
        agentType
    );


    // -----------------------------------------------------
    // GET TOKEN
    // -----------------------------------------------------

    const currentToken =
        localStorage.getItem(
            "access_token"
        );


    if (!currentToken) {

        window.location.href = "/";

        return;

    }


    // -----------------------------------------------------
    // SHOW USER MESSAGE
    // -----------------------------------------------------

    addChatMessage(
        "You",
        message,
        "user-message"
    );


    // -----------------------------------------------------
    // CLEAR INPUT
    // -----------------------------------------------------

    messageInput.value = "";


    // -----------------------------------------------------
    // SHOW LOADING
    // -----------------------------------------------------

    const loadingMessage =
        addChatMessage(
            "AI Agent",
            "Thinking...",
            "agent-message"
        );


    try {

        // -------------------------------------------------
        // SEND REQUEST
        // -------------------------------------------------

        const response =
            await fetch(
                "/agent/chat",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${currentToken}`

                    },

                    body:
                        JSON.stringify({

                            message:
                                message,

                            agent_type:
                                agentType

                        })

                }
            );


        console.log(
            "CHAT STATUS:",
            response.status
        );


        // -------------------------------------------------
        // AUTH ERROR
        // -------------------------------------------------

        if (
            response.status === 401
        ) {

            localStorage.clear();

            window.location.href = "/";

            return;

        }


        // -------------------------------------------------
        // API ERROR
        // -------------------------------------------------

        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);


            throw new Error(

                errorData?.detail ||
                "Chat request failed."

            );

        }


        // -------------------------------------------------
        // RESPONSE
        // -------------------------------------------------

        const data =
            await response.json();


        console.log(
            "CHAT DATA:",
            data
        );


        // -------------------------------------------------
        // REMOVE LOADING MESSAGE
        // -------------------------------------------------

        if (loadingMessage) {

            loadingMessage.remove();

        }


        // -------------------------------------------------
        // DISPLAY RESPONSE
        // -------------------------------------------------

        addChatMessage(

            data.agent ||
            "AI Agent",

            data.agent_response ||
            "No response received.",

            "agent-message"

        );


        console.log(
            "CHAT AGENT:",
            data.agent
        );


    }
    catch (error) {

        console.error(
            "CHAT ERROR:",
            error
        );


        if (loadingMessage) {

            loadingMessage.remove();

        }


        addChatMessage(

            "System",

            error.message,

            "agent-message error-message"

        );

    }

}


// =========================================================
// ADD CHAT MESSAGE
// =========================================================

function addChatMessage(
    sender,
    message,
    className
) {

    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    if (!chatMessages) {

        return null;

    }


    const messageElement =
        document.createElement(
            "div"
        );


    messageElement.className =
        className;


    messageElement.innerHTML = `

        <div class="chat-sender">

            ${escapeHtml(sender)}

        </div>

        <div class="chat-text">

            ${escapeHtml(message)}

        </div>

    `;


    chatMessages.appendChild(
        messageElement
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    return messageElement;

}


// =========================================================
// SEND BUTTON
// =========================================================

const sendButton =
    document.getElementById(
        "sendButton"
    );


if (sendButton) {

    sendButton.addEventListener(
        "click",
        sendChatMessage
    );

}


// =========================================================
// ENTER KEY
// =========================================================

const messageInput =
    document.getElementById(
        "messageInput"
    );


if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        function(event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendChatMessage();

            }

        }
    );

}