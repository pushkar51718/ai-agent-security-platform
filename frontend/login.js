// =========================================================
// LOGIN FORM
// =========================================================

const loginForm =
    document.getElementById("loginForm");

const loginError =
    document.getElementById("loginError");

const togglePassword =
    document.getElementById("togglePassword");

const passwordInput =
    document.getElementById("password");


// =========================================================
// SHOW / HIDE PASSWORD
// =========================================================

togglePassword.addEventListener(
    "click",
    () => {

        if (
            passwordInput.type ===
            "password"
        ) {

            passwordInput.type =
                "text";

            togglePassword.textContent =
                "Hide";

        } else {

            passwordInput.type =
                "password";

            togglePassword.textContent =
                "Show";
        }
    }
);


// =========================================================
// LOGIN
// =========================================================

loginForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        loginError.classList.add(
            "hidden"
        );


        const username =
            document
                .getElementById(
                    "username"
                )
                .value
                .trim();


        const password =
            passwordInput.value;


        try {

            const response =
                await fetch(
                    "/auth/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                username:
                                    username,

                                password:
                                    password
                            })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Invalid username or password"
                );
            }


            // ---------------------------------------------
            // SAVE AUTHENTICATION DATA
            // ---------------------------------------------

            localStorage.setItem(
                "access_token",
                data.access_token
            );


            localStorage.setItem(
                "username",
                data.username
            );


            localStorage.setItem(
                "role",
                data.role
            );


            // ---------------------------------------------
            // REDIRECT
            // ---------------------------------------------

            window.location.href =
                "/dashboard";

        } catch (error) {

            loginError.textContent =
                error.message;

            loginError.classList.remove(
                "hidden"
            );
        }

    }
);