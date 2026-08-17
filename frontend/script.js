// =========================================================
// AI AGENT SECURITY PLATFORM
// COMPLETE FRONTEND SCRIPT
// Authentication + Dashboard + Scanning + Reports
// + Persistent Admin User Management
// =========================================================


// =========================================================
// AUTHENTICATION STATE
// =========================================================

let token =
    localStorage.getItem("access_token");

let currentUsername =
    localStorage.getItem("username") || "User";

let currentRole =
    String(
        localStorage.getItem("role") || "user"
    )
        .toLowerCase()
        .trim();

let isAdmin =
    currentRole === "admin";


// =========================================================
// BASIC AUTH CHECK
// =========================================================

if (!token) {

    window.location.href = "/";

}


// =========================================================
// ELEMENTS
// =========================================================

const scanButton =
    document.getElementById("scanButton");

const agentSelect =
    document.getElementById("agentSelect");

const dashboard =
    document.getElementById("dashboard");

const loading =
    document.getElementById("loading");

const errorBox =
    document.getElementById("error");

const score =
    document.getElementById("score");

const risk =
    document.getElementById("risk");

const totalTests =
    document.getElementById("totalTests");

const passed =
    document.getElementById("passed");

const failed =
    document.getElementById("failed");

const resultsContainer =
    document.getElementById("results");

const logoutButton =
    document.getElementById("logoutButton");

const refreshHistory =
    document.getElementById("refreshHistory");

const loggedUsername =
    document.getElementById("loggedUsername");

const loggedRole =
    document.getElementById("loggedRole");

const downloadReport =
    document.getElementById("downloadReport");

const downloadPdfReport =
    document.getElementById("downloadPdfReport");

const refreshAnalytics =
    document.getElementById("refreshAnalytics");

const openChatButton =
    document.getElementById("openChatButton");


// =========================================================
// REPORT STATE
// =========================================================

let latestReportFile = null;

let latestPdfReportFile = null;


// =========================================================
// UPDATE USER DISPLAY
// =========================================================

function updateUserDisplay() {

    if (loggedUsername) {

        loggedUsername.textContent =
            currentUsername;

    }

    if (loggedRole) {

        loggedRole.textContent =
            currentRole;

    }

}


// =========================================================
// LOGOUT
// =========================================================

function logout() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "username"
    );

    localStorage.removeItem(
        "role"
    );

    window.location.href = "/";

}


if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        logout
    );

}


// =========================================================
// AI CHAT BUTTON
// =========================================================

if (openChatButton) {

    openChatButton.addEventListener(
        "click",
        function () {

            window.location.href =
                "/chat";

        }
    );

}


// =========================================================
// AUTHENTICATION VERIFICATION
// =========================================================

async function verifyAuthentication() {

    const currentToken =
        localStorage.getItem(
            "access_token"
        );

    if (!currentToken) {

        logout();

        return false;

    }

    try {

        const response =
            await fetch(
                "/auth/me",
                {

                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${currentToken}`

                    }

                }
            );


        if (response.status === 401) {

            logout();

            return false;

        }


        if (!response.ok) {

            console.error(
                "Authentication verification failed:",
                response.status
            );

            return false;

        }


        const data =
            await response.json();


        console.log(
            "AUTHENTICATED USER:",
            data
        );


        if (data.username) {

            currentUsername =
                data.username;

            localStorage.setItem(
                "username",
                data.username
            );

        }


        if (data.role) {

            currentRole =
                String(data.role)
                    .toLowerCase()
                    .trim();

            localStorage.setItem(
                "role",
                data.role
            );

        }


        isAdmin =
            currentRole === "admin";


        token =
            currentToken;


        updateUserDisplay();


        return true;


    }
    catch (error) {

        console.error(
            "AUTH VERIFICATION ERROR:",
            error
        );

        return false;

    }

}


// =========================================================
// ADMIN BUTTON
// =========================================================

function createAdminButton() {

    if (!isAdmin) {

        return;

    }


    if (
        document.getElementById(
            "adminPanelButton"
        )
    ) {

        return;

    }


    let header =
        document.querySelector("header");


    if (!header) {

        header =
            document.querySelector(
                ".header"
            );

    }


    if (!header) {

        console.log(
            "Header not found. Creating admin button near top of page."
        );

        return;

    }


    const button =
        document.createElement(
            "button"
        );


    button.id =
        "adminPanelButton";


    button.type =
        "button";


    button.textContent =
        "👑 ADMIN";


    button.style.marginLeft =
        "10px";


    button.style.background =
        "#7c3aed";


    button.style.color =
        "#ffffff";


    button.style.border =
        "none";


    button.style.padding =
        "12px 18px";


    button.style.borderRadius =
        "8px";


    button.style.cursor =
        "pointer";


    button.style.fontWeight =
        "bold";


    button.addEventListener(
        "click",
        openAdminPanel
    );


    header.appendChild(
        button
    );

}


// =========================================================
// ADMIN API HELPER
// =========================================================

async function adminRequest(
    url,
    options = {}
) {

    const currentToken =
        localStorage.getItem(
            "access_token"
        );


    if (!currentToken) {

        logout();

        throw new Error(
            "Authentication required."
        );

    }


    const headers = {

        ...(options.headers || {}),

        "Authorization":
            `Bearer ${currentToken}`

    };


    if (
        options.body &&
        !headers["Content-Type"]
    ) {

        headers["Content-Type"] =
            "application/json";

    }


    const response =
        await fetch(
            url,
            {

                ...options,

                headers

            }
        );


    if (response.status === 401) {

        logout();

        throw new Error(
            "Your session has expired. Please login again."
        );

    }


    if (response.status === 403) {

        throw new Error(
            "Administrator privileges required."
        );

    }


    return response;

}


// =========================================================
// OPEN ADMIN PANEL
// =========================================================

async function openAdminPanel() {

    if (!isAdmin) {

        alert(
            "Administrator privileges required."
        );

        return;

    }


    try {

        const response =
            await adminRequest(
                "/admin/users",
                {

                    method: "GET"

                }
            );


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(
                        () => null
                    );


            throw new Error(
                errorData?.detail ||
                "Unable to load administrator information."
            );

        }


        const data =
            await response.json();


        showAdminModal(
            data
        );


    }
    catch (error) {

        console.error(
            "ADMIN PANEL ERROR:",
            error
        );


        alert(
            error.message
        );

    }

}


// =========================================================
// ADMIN MODAL
// =========================================================

function showAdminModal(data) {

    const oldModal =
        document.getElementById(
            "adminModal"
        );


    if (oldModal) {

        oldModal.remove();

    }


    const modal =
        document.createElement(
            "div"
        );


    modal.id =
        "adminModal";


    Object.assign(
        modal.style,
        {

            position: "fixed",

            inset: "0",

            background:
                "rgba(0,0,0,0.78)",

            display: "flex",

            alignItems: "center",

            justifyContent: "center",

            zIndex: "99999",

            padding: "20px"

        }
    );


    const content =
        document.createElement(
            "div"
        );


    Object.assign(
        content.style,
        {

            background: "#1e293b",

            color: "#ffffff",

            width: "850px",

            maxWidth: "95vw",

            maxHeight: "90vh",

            overflowY: "auto",

            borderRadius: "14px",

            padding: "30px",

            boxShadow:
                "0 25px 60px rgba(0,0,0,0.6)"

        }
    );


    // =====================================================
    // TITLE
    // =====================================================

    const title =
        document.createElement(
            "h2"
        );


    title.textContent =
        "👑 Administrator Panel";


    title.style.marginTop =
        "0";


    title.style.fontSize =
        "32px";


    content.appendChild(
        title
    );


    // =====================================================
    // CURRENT USER
    // =====================================================

    const current =
        document.createElement(
            "p"
        );


    current.textContent =
        `Logged in as: ${currentUsername} | Role: ADMIN`;


    current.style.color =
        "#4ade80";


    current.style.fontSize =
        "20px";


    content.appendChild(
        current
    );


    // =====================================================
    // USER LIST
    // =====================================================

    const userList =
        Array.isArray(data.users)
            ? data.users
            : [];


    const count =
        document.createElement(
            "p"
        );


    count.id =
        "adminUserCount";


    count.textContent =
        `Total users: ${userList.length}`;


    count.style.fontSize =
        "20px";


    content.appendChild(
        count
    );


    // =====================================================
    // USERS TABLE
    // =====================================================

    const table =
        document.createElement(
            "table"
        );


    Object.assign(
        table.style,
        {

            width: "100%",

            borderCollapse:
                "collapse",

            marginTop: "15px"

        }
    );


    const thead =
        document.createElement(
            "thead"
        );


    thead.innerHTML = `

        <tr>

            <th style="
                text-align:left;
                padding:12px;
                border-bottom:1px solid #64748b;
            ">
                Username
            </th>

            <th style="
                text-align:left;
                padding:12px;
                border-bottom:1px solid #64748b;
            ">
                Role
            </th>

            <th style="
                text-align:center;
                padding:12px;
                border-bottom:1px solid #64748b;
            ">
                Actions
            </th>

        </tr>

    `;


    table.appendChild(
        thead
    );


    const tbody =
        document.createElement(
            "tbody"
        );


    tbody.id =
        "adminUsersTableBody";


    table.appendChild(
        tbody
    );


    content.appendChild(
        table
    );


    renderAdminUsers(
        tbody,
        userList
    );


    // =====================================================
    // ADD USER SECTION
    // =====================================================

    const addTitle =
        document.createElement(
            "h3"
        );


    addTitle.textContent =
        "➕ Add User";


    addTitle.style.marginTop =
        "35px";


    addTitle.style.fontSize =
        "24px";


    content.appendChild(
        addTitle
    );


    const addForm =
        document.createElement(
            "form"
        );


    addForm.id =
        "adminCreateUserForm";


    addForm.autocomplete =
        "off";


    // -----------------------------------------------------
    // USERNAME
    // -----------------------------------------------------

    const usernameInput =
        document.createElement(
            "input"
        );


    usernameInput.type =
        "text";


    usernameInput.id =
        "adminNewUsername";


    usernameInput.placeholder =
        "Username";


    usernameInput.autocomplete =
        "off";


    styleAdminInput(
        usernameInput
    );


    addForm.appendChild(
        usernameInput
    );


    // -----------------------------------------------------
    // PASSWORD
    // -----------------------------------------------------

    const passwordInput =
        document.createElement(
            "input"
        );


    passwordInput.type =
        "password";


    passwordInput.id =
        "adminNewPassword";


    passwordInput.placeholder =
        "Password";


    passwordInput.autocomplete =
        "new-password";


    styleAdminInput(
        passwordInput
    );


    addForm.appendChild(
        passwordInput
    );


    // -----------------------------------------------------
    // ROLE
    // -----------------------------------------------------

    const roleSelect =
        document.createElement(
            "select"
        );


    roleSelect.id =
        "adminNewRole";


    roleSelect.innerHTML = `

        <option value="user">
            user
        </option>

        <option value="security_analyst">
            security_analyst
        </option>

        <option value="admin">
            admin
        </option>

    `;


    styleAdminInput(
        roleSelect
    );


    addForm.appendChild(
        roleSelect
    );


    // -----------------------------------------------------
    // CREATE BUTTON
    // -----------------------------------------------------

    const createButton =
        document.createElement(
            "button"
        );


    createButton.type =
        "submit";


    createButton.textContent =
        "CREATE USER";


    Object.assign(
        createButton.style,
        {

            width: "100%",

            padding: "14px",

            marginTop: "10px",

            background: "#16a34a",

            color: "white",

            border: "none",

            borderRadius: "8px",

            cursor: "pointer",

            fontWeight: "bold",

            fontSize: "16px"

        }
    );


    addForm.appendChild(
        createButton
    );


    // -----------------------------------------------------
    // CREATE STATUS
    // -----------------------------------------------------

    const createStatus =
        document.createElement(
            "div"
        );


    createStatus.id =
        "adminCreateStatus";


    createStatus.style.marginTop =
        "12px";


    addForm.appendChild(
        createStatus
    );


    // -----------------------------------------------------
    // CREATE EVENT
    // -----------------------------------------------------

    addForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const newUsername =
                usernameInput.value.trim();


            const newPassword =
                passwordInput.value;


            const newRole =
                roleSelect.value;


            if (!newUsername) {

                createStatus.textContent =
                    "Username is required.";

                createStatus.style.color =
                    "#f87171";

                return;

            }


            if (!newPassword) {

                createStatus.textContent =
                    "Password is required.";

                createStatus.style.color =
                    "#f87171";

                return;

            }


            if (newPassword.length < 6) {

                createStatus.textContent =
                    "Password must contain at least 6 characters.";

                createStatus.style.color =
                    "#f87171";

                return;

            }


            createButton.disabled =
                true;


            createButton.textContent =
                "CREATING...";


            createStatus.textContent =
                "";


            try {

                const response =
                    await adminRequest(
                        "/admin/users",
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify({

                                    username:
                                        newUsername,

                                    password:
                                        newPassword,

                                    role:
                                        newRole

                                })

                        }
                    );


                const result =
                    await response
                        .json()
                        .catch(
                            () => ({})
                        );


                if (!response.ok) {

                    throw new Error(
                        result.detail ||
                        "Unable to create user."
                    );

                }


                createStatus.textContent =
                    "✓ User created successfully.";


                createStatus.style.color =
                    "#4ade80";


                usernameInput.value =
                    "";


                passwordInput.value =
                    "";


                roleSelect.value =
                    "user";


                // Refresh admin panel
                await refreshAdminPanel(
                    modal
                );


            }
            catch (error) {

                console.error(
                    "CREATE USER ERROR:",
                    error
                );


                createStatus.textContent =
                    error.message;


                createStatus.style.color =
                    "#f87171";

            }
            finally {

                createButton.disabled =
                    false;

                createButton.textContent =
                    "CREATE USER";

            }

        }
    );


    content.appendChild(
        addForm
    );


    // =====================================================
    // CLOSE BUTTON
    // =====================================================

    const closeButton =
        document.createElement(
            "button"
        );


    closeButton.type =
        "button";


    closeButton.textContent =
        "CLOSE";


    Object.assign(
        closeButton.style,
        {

            marginTop: "25px",

            padding: "12px 25px",

            background: "#2563eb",

            color: "white",

            border: "none",

            borderRadius: "8px",

            cursor: "pointer",

            fontWeight: "bold"

        }
    );


    closeButton.addEventListener(
        "click",
        function() {

            modal.remove();

        }
    );


    content.appendChild(
        closeButton
    );


    modal.appendChild(
        content
    );


    document.body.appendChild(
        modal
    );


    // Close when clicking outside
    modal.addEventListener(
        "click",
        function(event) {

            if (
                event.target === modal
            ) {

                modal.remove();

            }

        }
    );

}


// =========================================================
// STYLE ADMIN INPUT
// =========================================================

function styleAdminInput(element) {

    Object.assign(
        element.style,
        {

            width: "100%",

            boxSizing: "border-box",

            padding: "14px",

            marginTop: "12px",

            background: "#0f172a",

            color: "#ffffff",

            border:
                "1px solid #475569",

            borderRadius: "8px",

            fontSize: "16px"

        }
    );

}


// =========================================================
// RENDER ADMIN USERS
// =========================================================

function renderAdminUsers(
    tbody,
    users
) {

    tbody.innerHTML =
        "";


    if (
        !Array.isArray(users) ||
        users.length === 0
    ) {

        const row =
            document.createElement(
                "tr"
            );


        row.innerHTML = `

            <td colspan="3"
                style="
                    padding:20px;
                    text-align:center;
                    color:#94a3b8;
                "
            >
                No users found.
            </td>

        `;


        tbody.appendChild(
            row
        );


        return;

    }


    users.forEach(
        user => {

            const row =
                document.createElement(
                    "tr"
                );


            const usernameCell =
                document.createElement(
                    "td"
                );


            usernameCell.textContent =
                user.username;


            Object.assign(
                usernameCell.style,
                {

                    padding: "12px",

                    borderBottom:
                        "1px solid #334155",

                    fontWeight:
                        "bold"

                }
            );


            const roleCell =
                document.createElement(
                    "td"
                );


            roleCell.style.padding =
                "12px";


            roleCell.style.borderBottom =
                "1px solid #334155";


            const roleSelect =
                document.createElement(
                    "select"
                );


            roleSelect.innerHTML = `

                <option value="user">
                    user
                </option>

                <option value="security_analyst">
                    security_analyst
                </option>

                <option value="admin">
                    admin
                </option>

            `;


            roleSelect.value =
                user.role;


            Object.assign(
                roleSelect.style,
                {

                    background: "#0f172a",

                    color: "#ffffff",

                    border:
                        "1px solid #475569",

                    borderRadius: "6px",

                    padding: "8px"

                }
            );


            roleCell.appendChild(
                roleSelect
            );


            const actionCell =
                document.createElement(
                    "td"
                );


            Object.assign(
                actionCell.style,
                {

                    padding: "12px",

                    borderBottom:
                        "1px solid #334155",

                    textAlign: "center"

                }
            );


            // =================================================
            // UPDATE ROLE BUTTON
            // =================================================

            const updateButton =
                document.createElement(
                    "button"
                );


            updateButton.type =
                "button";


            updateButton.textContent =
                "UPDATE ROLE";


            Object.assign(
                updateButton.style,
                {

                    background: "#2563eb",

                    color: "#ffffff",

                    border: "none",

                    borderRadius: "6px",

                    padding: "8px 12px",

                    cursor: "pointer",

                    fontWeight: "bold",

                    marginRight: "8px"

                }
            );


            // =================================================
            // PREVENT SELF ROLE CHANGE
            // =================================================

            if (
                user.username ===
                currentUsername
            ) {

                roleSelect.value =
                    "admin";

            }


            updateButton.addEventListener(
                "click",
                async function() {

                    const selectedRole =
                        roleSelect.value;


                    if (
                        user.username ===
                        currentUsername &&
                        selectedRole !== "admin"
                    ) {

                        alert(
                            "You cannot remove your own administrator role."
                        );

                        roleSelect.value =
                            "admin";

                        return;

                    }


                    const confirmed =
                        confirm(
                            `Change role of "${user.username}" to "${selectedRole}"?`
                        );


                    if (!confirmed) {

                        return;

                    }


                    updateButton.disabled =
                        true;


                    updateButton.textContent =
                        "UPDATING...";


                    try {

                        const response =
                            await adminRequest(
                                `/admin/users/${encodeURIComponent(
                                    user.username
                                )}/role`,
                                {

                                    method: "PUT",

                                    headers: {

                                        "Content-Type":
                                            "application/json"

                                    },

                                    body:
                                        JSON.stringify({

                                            role:
                                                selectedRole

                                        })

                                }
                            );


                        const result =
                            await response
                                .json()
                                .catch(
                                    () => ({})
                                );


                        if (!response.ok) {

                            throw new Error(
                                result.detail ||
                                "Unable to update role."
                            );

                        }


                        alert(
                            "User role updated successfully."
                        );


                        await refreshAdminPanel(
                            document.getElementById(
                                "adminModal"
                            )
                        );


                    }
                    catch (error) {

                        console.error(
                            "UPDATE ROLE ERROR:",
                            error
                        );


                        alert(
                            error.message
                        );

                    }
                    finally {

                        updateButton.disabled =
                            false;

                        updateButton.textContent =
                            "UPDATE ROLE";

                    }

                }
            );


            // =================================================
            // DELETE BUTTON
            // =================================================

            const deleteButton =
                document.createElement(
                    "button"
                );


            deleteButton.type =
                "button";


            deleteButton.textContent =
                "DELETE";


            Object.assign(
                deleteButton.style,
                {

                    background: "#dc2626",

                    color: "#ffffff",

                    border: "none",

                    borderRadius: "6px",

                    padding: "8px 12px",

                    cursor: "pointer",

                    fontWeight: "bold"

                }
            );


            // Don't allow deleting yourself
            if (
                user.username ===
                currentUsername
            ) {

                deleteButton.disabled =
                    true;


                deleteButton.title =
                    "You cannot delete your own administrator account.";


                deleteButton.style.opacity =
                    "0.45";


                deleteButton.style.cursor =
                    "not-allowed";

            }


            deleteButton.addEventListener(
                "click",
                async function() {

                    if (
                        user.username ===
                        currentUsername
                    ) {

                        alert(
                            "You cannot delete your own administrator account."
                        );

                        return;

                    }


                    const confirmed =
                        confirm(
                            `Are you sure you want to permanently delete "${user.username}"?`
                        );


                    if (!confirmed) {

                        return;

                    }


                    deleteButton.disabled =
                        true;


                    deleteButton.textContent =
                        "DELETING...";


                    try {

                        const response =
                            await adminRequest(
                                `/admin/users/${encodeURIComponent(
                                    user.username
                                )}`,
                                {

                                    method: "DELETE"

                                }
                            );


                        const result =
                            await response
                                .json()
                                .catch(
                                    () => ({})
                                );


                        if (!response.ok) {

                            throw new Error(
                                result.detail ||
                                "Unable to delete user."
                            );

                        }


                        alert(
                            "User deleted successfully."
                        );


                        await refreshAdminPanel(
                            document.getElementById(
                                "adminModal"
                            )
                        );


                    }
                    catch (error) {

                        console.error(
                            "DELETE USER ERROR:",
                            error
                        );


                        alert(
                            error.message
                        );


                    }
                    finally {

                        deleteButton.disabled =
                            false;

                        deleteButton.textContent =
                            "DELETE";

                    }

                }
            );


            actionCell.appendChild(
                updateButton
            );


            actionCell.appendChild(
                deleteButton
            );


            row.appendChild(
                usernameCell
            );


            row.appendChild(
                roleCell
            );


            row.appendChild(
                actionCell
            );


            tbody.appendChild(
                row
            );

        }
    );

}


// =========================================================
// REFRESH ADMIN PANEL
// =========================================================

async function refreshAdminPanel(
    modal
) {

    if (!modal) {

        return;

    }


    try {

        const response =
            await adminRequest(
                "/admin/users",
                {

                    method: "GET"

                }
            );


        if (!response.ok) {

            throw new Error(
                "Unable to refresh users."
            );

        }


        const data =
            await response.json();


        const tbody =
            modal.querySelector(
                "#adminUsersTableBody"
            );


        if (tbody) {

            renderAdminUsers(
                tbody,
                Array.isArray(data.users)
                    ? data.users
                    : []
            );

        }


        const count =
            modal.querySelector(
                "#adminUserCount"
            );


        if (count) {

            count.textContent =
                `Total users: ${
                    Array.isArray(data.users)
                        ? data.users.length
                        : 0
                }`;

        }


    }
    catch (error) {

        console.error(
            "ADMIN REFRESH ERROR:",
            error
        );

        alert(
            error.message
        );

    }

}


// =========================================================
// SECURITY SCAN BUTTON
// =========================================================

if (scanButton) {

    scanButton.addEventListener(
        "click",
        runScan
    );

}


// =========================================================
// RUN SECURITY SCAN
// =========================================================

async function runScan() {

    if (!agentSelect) {

        console.error(
            "agentSelect element not found."
        );

        return;

    }


    const agentType =
        agentSelect.value;


    if (!agentType) {

        alert(
            "Please select an AI agent."
        );

        return;

    }


    if (errorBox) {

        errorBox.classList.add(
            "hidden"
        );

    }


    if (dashboard) {

        dashboard.classList.add(
            "hidden"
        );

    }


    if (loading) {

        loading.classList.remove(
            "hidden"
        );

    }


    if (scanButton) {

        scanButton.disabled =
            true;

    }


    latestReportFile =
        null;


    latestPdfReportFile =
        null;


    if (downloadReport) {

        downloadReport.disabled =
            true;

    }


    if (downloadPdfReport) {

        downloadPdfReport.disabled =
            true;

    }


    try {

        console.log(
            "STARTING SECURITY SCAN:",
            agentType
        );


        const currentToken =
            localStorage.getItem(
                "access_token"
            );


        const response =
            await fetch(
                `/security/scan/${encodeURIComponent(
                    agentType
                )}`,
                {

                    method: "POST",

                    headers: {

                        "Authorization":
                            `Bearer ${currentToken}`

                    }

                }
            );


        console.log(
            "SCAN STATUS:",
            response.status
        );


        if (response.status === 401) {

            logout();

            return;

        }


        if (response.status === 403) {

            throw new Error(
                "You do not have permission to run this security scan."
            );

        }


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(
                        () => null
                    );


            throw new Error(
                errorData?.detail ||
                "Security scan failed."
            );

        }


        const data =
            await response.json();


        console.log(
            "SCAN DATA:",
            data
        );


        displayResults(
            data
        );


        await loadHistory();

        await loadAnalytics();


        console.log(
            "SECURITY SCAN COMPLETED"
        );


    }
    catch (error) {

        console.error(
            "SCAN ERROR:",
            error
        );


        if (errorBox) {

            errorBox.textContent =
                error.message;


            errorBox.classList.remove(
                "hidden"
            );

        }
        else {

            alert(
                error.message
            );

        }

    }
    finally {

        if (loading) {

            loading.classList.add(
                "hidden"
            );

        }


        if (scanButton) {

            scanButton.disabled =
                false;

        }

    }

}


// =========================================================
// DISPLAY SCAN RESULTS
// =========================================================

function displayResults(data) {

    if (dashboard) {

        dashboard.classList.remove(
            "hidden"
        );

    }


    if (score) {

        score.textContent =
            `${data.security_score ?? 0}/10`;

    }


    if (risk) {

        risk.textContent =
            data.risk_level ?? "UNKNOWN";

    }


    if (totalTests) {

        totalTests.textContent =
            data.total_tests ?? 0;

    }


    if (passed) {

        passed.textContent =
            data.passed ?? 0;

    }


    if (failed) {

        failed.textContent =
            data.failed ?? 0;

    }


    latestReportFile =
        data.report_file ||
        null;


    latestPdfReportFile =
        data.pdf_report_file ||
        null;


    if (downloadReport) {

        downloadReport.disabled =
            !latestReportFile;

    }


    if (downloadPdfReport) {

        downloadPdfReport.disabled =
            !latestPdfReportFile;

    }


    if (!resultsContainer) {

        return;

    }


    resultsContainer.innerHTML =
        "";


    const testResults =
        Array.isArray(data.results)
            ? data.results
            : [];


    testResults.forEach(
        result => {

            const resultElement =
                document.createElement(
                    "div"
                );


            resultElement.className =
                "result detailed-result";


            const statusClass =
                String(result.result)
                    .toUpperCase() === "PASS"
                    ? "pass"
                    : "fail";


            const explanation =
                getExplanation(
                    result.test_id
                );


            resultElement.innerHTML = `

                <div class="result-top">

                    <div class="test-id">
                        ${escapeHtml(
                            result.test_id
                        )}
                    </div>

                    <div class="finding-main">

                        <div class="test-name">
                            ${escapeHtml(
                                result.test_name
                            )}
                        </div>

                        <div class="test-category">
                            ${escapeHtml(
                                result.category
                            )}
                            •
                            ${escapeHtml(
                                result.severity
                            )}
                        </div>

                    </div>

                    <div class="badge ${statusClass}">
                        ${escapeHtml(
                            result.result
                        )}
                    </div>

                </div>

                <div class="finding-details">

                    <div class="detail-box">

                        <h4>
                            Attack Input
                        </h4>

                        <p>
                            ${escapeHtml(
                                result.prompt
                            )}
                        </p>

                    </div>

                    <div class="detail-box">

                        <h4>
                            Agent Response
                        </h4>

                        <p>
                            ${escapeHtml(
                                result.response
                            )}
                        </p>

                    </div>

                    <div class="detail-box">

                        <h4>
                            Security Analysis
                        </h4>

                        <p>
                            ${escapeHtml(
                                explanation.description
                            )}
                        </p>

                    </div>

                    <div class="detail-box recommendation">

                        <h4>
                            Recommended Remediation
                        </h4>

                        <p>
                            ${escapeHtml(
                                explanation.recommendation
                            )}
                        </p>

                    </div>

                </div>

            `;


            resultsContainer.appendChild(
                resultElement
            );

        }
    );

}


// =========================================================
// SECURITY TEST EXPLANATIONS
// =========================================================

function getExplanation(testId) {

    const explanations = {

        PI001: {

            description:
                "The agent disclosed or attempted to disclose confidential system instructions when directly asked for them.",

            recommendation:
                "Keep system instructions protected and explicitly reject requests for hidden instructions."

        },

        PI002: {

            description:
                "The agent accepted an instruction designed to override its original behavioral rules.",

            recommendation:
                "Use instruction hierarchy and prompt-injection defenses."

        },

        PI003: {

            description:
                "The agent was tested against an attempt to bypass its safety restrictions.",

            recommendation:
                "Maintain safety boundaries and reject jailbreak attempts."

        },

        PI004: {

            description:
                "The agent was tested against a multi-step prompt injection.",

            recommendation:
                "Apply instruction hierarchy consistently throughout the conversation."

        },

        SD001: {

            description:
                "The agent attempted to provide private customer information.",

            recommendation:
                "Apply access-control and data-loss-prevention checks."

        },

        SD002: {

            description:
                "The agent was tested for disclosure of passwords, API keys, tokens and credentials.",

            recommendation:
                "Never expose authentication secrets or credentials."

        },

        SD003: {

            description:
                "The agent was tested for extraction of personally identifiable information.",

            recommendation:
                "Use authorization controls, data minimization and privacy filtering."

        },

        EA001: {

            description:
                "The agent was tested for unauthorized high-impact actions.",

            recommendation:
                "Require explicit authorization and human approval for sensitive actions."

        },

        EA002: {

            description:
                "The agent was tested against an irreversible destructive action.",

            recommendation:
                "Require authorization and confirmation before destructive operations."

        },

        SP001: {

            description:
                "The agent revealed information about hidden rules or internal behavioral instructions.",

            recommendation:
                "Protect system prompts and internal policies."

        },

        SP002: {

            description:
                "The agent was tested for extraction of hidden configuration and developer instructions.",

            recommendation:
                "Protect developer instructions and internal configuration."

        },

        RA001: {

            description:
                "The agent was tested for unauthorized access to administrator-only records and controls.",

            recommendation:
                "Enforce role-based access control before exposing administrative functionality."

        }

    };


    return (
        explanations[testId] ||
        {

            description:
                "The security test identified behavior that requires further investigation.",

            recommendation:
                "Review the agent instructions, authorization controls and response filtering."

        }
    );

}


// =========================================================
// HTML ESCAPING
// =========================================================

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text ?? "";


    return div.innerHTML;

}


// =========================================================
// SCAN HISTORY
// =========================================================

async function loadHistory() {

    const historyBody =
        document.getElementById(
            "historyBody"
        );


    if (!historyBody) {

        return;

    }


    const currentToken =
        localStorage.getItem(
            "access_token"
        );


    if (!currentToken) {

        logout();

        return;

    }


    historyBody.innerHTML = `

        <tr>

            <td colspan="9">
                Loading scan history...
            </td>

        </tr>

    `;


    try {

        const response =
            await fetch(
                "/security/history",
                {

                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${currentToken}`

                    }

                }
            );


        if (response.status === 401) {

            logout();

            return;

        }


        if (response.status === 403) {

            throw new Error(
                "You do not have permission to view scan history."
            );

        }


        if (!response.ok) {

            throw new Error(
                `History API returned ${response.status}`
            );

        }


        const data =
            await response.json();


        historyBody.innerHTML =
            "";


        if (
            !data.history ||
            data.history.length === 0
        ) {

            historyBody.innerHTML = `

                <tr>

                    <td colspan="9">
                        No scan history available.
                    </td>

                </tr>

            `;

            return;

        }


        data.history.forEach(
            scan => {

                const row =
                    document.createElement(
                        "tr"
                    );


                const riskClass =
                    String(
                        scan.risk_level || ""
                    )
                        .toLowerCase()
                        .replace(
                            /\s+/g,
                            "-"
                        );


                row.innerHTML = `

                    <td>
                        ${escapeHtml(
                            scan.created_at
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            scan.username ||
                            currentUsername
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            scan.agent
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            scan.security_score
                        )}/10
                    </td>

                    <td>

                        <span class="
                            history-risk
                            ${riskClass}
                        ">
                            ${escapeHtml(
                                scan.risk_level
                            )}
                        </span>

                    </td>

                    <td>
                        ${escapeHtml(
                            scan.total_tests
                        )}
                    </td>

                    <td class="history-pass">
                        ${escapeHtml(
                            scan.passed
                        )}
                    </td>

                    <td class="history-fail">
                        ${escapeHtml(
                            scan.failed
                        )}
                    </td>

                    <td>
                        ${
                            isAdmin
                                ? `
                                    <span style="
                                        color:#a78bfa;
                                        font-weight:bold;
                                    ">
                                        ADMIN VIEW
                                    </span>
                                  `
                                : ""
                        }
                    </td>

                `;


                historyBody.appendChild(
                    row
                );

            }
        );


    }
    catch (error) {

        console.error(
            "HISTORY LOAD ERROR:",
            error
        );


        historyBody.innerHTML = `

            <tr>

                <td colspan="9">
                    Failed to load scan history.
                </td>

            </tr>

        `;

    }

}


// =========================================================
// REFRESH HISTORY
// =========================================================

if (refreshHistory) {

    refreshHistory.addEventListener(
        "click",
        loadHistory
    );

}


// =========================================================
// DOWNLOAD SECURITY REPORT
// =========================================================

if (downloadReport) {

    downloadReport.addEventListener(
        "click",
        downloadLatestReport
    );

}


async function downloadLatestReport() {

    if (!latestReportFile) {

        alert(
            "Please run a security scan first."
        );

        return;

    }


    const currentToken =
        localStorage.getItem(
            "access_token"
        );


    if (!currentToken) {

        logout();

        return;

    }


    try {

        const response =
            await fetch(
                `/security/report/${encodeURIComponent(
                    latestReportFile
                )}`,
                {

                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${currentToken}`

                    }

                }
            );


        if (response.status === 401) {

            logout();

            return;

        }


        if (!response.ok) {

            throw new Error(
                "Unable to download security report."
            );

        }


        const blob =
            await response.blob();


        const url =
            window.URL.createObjectURL(
                blob
            );


        const link =
            document.createElement(
                "a"
            );


        link.href =
            url;


        link.download =
            latestReportFile;


        document.body.appendChild(
            link
        );


        link.click();


        link.remove();


        window.URL.revokeObjectURL(
            url
        );


    }
    catch (error) {

        console.error(
            "REPORT DOWNLOAD ERROR:",
            error
        );


        alert(
            error.message
        );

    }

}


// =========================================================
// DOWNLOAD PDF REPORT
// =========================================================

if (downloadPdfReport) {

    downloadPdfReport.addEventListener(
        "click",
        downloadLatestPdfReport
    );

}


async function downloadLatestPdfReport() {

    if (!latestPdfReportFile) {

        alert(
            "Please run a security scan first."
        );

        return;

    }


    const currentToken =
        localStorage.getItem(
            "access_token"
        );


    if (!currentToken) {

        logout();

        return;

    }


    try {

        const response =
            await fetch(
                `/security/report/${encodeURIComponent(
                    latestPdfReportFile
                )}`,
                {

                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${currentToken}`

                    }

                }
            );


        if (response.status === 401) {

            logout();

            return;

        }


        if (!response.ok) {

            throw new Error(
                "Unable to download PDF report."
            );

        }


        const blob =
            await response.blob();


        const url =
            window.URL.createObjectURL(
                blob
            );


        const link =
            document.createElement(
                "a"
            );


        link.href =
            url;


        link.download =
            latestPdfReportFile;


        document.body.appendChild(
            link
        );


        link.click();


        link.remove();


        window.URL.revokeObjectURL(
            url
        );


    }
    catch (error) {

        console.error(
            "PDF DOWNLOAD ERROR:",
            error
        );


        alert(
            error.message
        );

    }

}


// =========================================================
// DASHBOARD ANALYTICS
// =========================================================

async function loadAnalytics() {

    const totalScans =
        document.getElementById(
            "analyticsTotalScans"
        );

    const secureScans =
        document.getElementById(
            "analyticsSecureScans"
        );

    const vulnerableScans =
        document.getElementById(
            "analyticsVulnerableScans"
        );

    const averageScore =
        document.getElementById(
            "analyticsAverageScore"
        );

    const critical =
        document.getElementById(
            "analyticsCritical"
        );

    const high =
        document.getElementById(
            "analyticsHigh"
        );

    const medium =
        document.getElementById(
            "analyticsMedium"
        );

    const low =
        document.getElementById(
            "analyticsLow"
        );


    if (
        !totalScans ||
        !secureScans ||
        !vulnerableScans ||
        !averageScore ||
        !critical ||
        !high ||
        !medium ||
        !low
    ) {

        return;

    }


    const currentToken =
        localStorage.getItem(
            "access_token"
        );


    if (!currentToken) {

        logout();

        return;

    }


    try {

        const response =
            await fetch(
                "/security/analytics",
                {

                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${currentToken}`

                    }

                }
            );


        if (response.status === 401) {

            logout();

            return;

        }


        if (!response.ok) {

            throw new Error(
                "Unable to load analytics."
            );

        }


        const data =
            await response.json();


        totalScans.textContent =
            data.total_scans ?? 0;


        secureScans.textContent =
            data.secure_scans ?? 0;


        vulnerableScans.textContent =
            data.vulnerable_scans ?? 0;


        averageScore.textContent =
            `${data.average_score ?? 0}/10`;


        critical.textContent =
            data.critical ?? 0;


        high.textContent =
            data.high ?? 0;


        medium.textContent =
            data.medium ?? 0;


        low.textContent =
            data.low ?? 0;


    }
    catch (error) {

        console.error(
            "ANALYTICS LOAD ERROR:",
            error
        );

    }

}


// =========================================================
// REFRESH ANALYTICS
// =========================================================

if (refreshAnalytics) {

    refreshAnalytics.addEventListener(
        "click",
        loadAnalytics
    );

}


// =========================================================
// INITIALIZE APPLICATION
// =========================================================

async function initializeApplication() {

    console.log(
        "======================================"
    );

    console.log(
        "AI AGENT SECURITY PLATFORM"
    );

    console.log(
        "======================================"
    );


    const authenticated =
        await verifyAuthentication();


    if (!authenticated) {

        return;

    }


    console.log(
        "Username:",
        currentUsername
    );


    console.log(
        "Role:",
        currentRole
    );


    console.log(
        "Is Admin:",
        isAdmin
    );


    console.log(
        "Authentication:",
        token ? "ACTIVE" : "MISSING"
    );


    console.log(
        "======================================"
    );


    // Create admin button AFTER
    // authentication has been verified.
    createAdminButton();


    // Load dashboard information.
    await loadHistory();

    await loadAnalytics();

}


// =========================================================
// START APPLICATION
// =========================================================

initializeApplication();