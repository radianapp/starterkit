/**
 * WebAuthn (Passkeys) Helper Functions
 */

// --- Base64URL Helpers ---
function bufferToBase64url(buffer) {
    const bytes = new Uint8Array(buffer);
    let str = "";
    for (let charCode of bytes) {
        str += String.fromCharCode(charCode);
    }
    const base64 = btoa(str);
    return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
}

function base64urlToBuffer(base64url) {
    const padding = "==".slice(0, (4 - (base64url.length % 4)) % 4);
    const base64 = (base64url + padding).replace(/-/g, "+").replace(/_/g, "/");
    const str = atob(base64);
    const buffer = new ArrayBuffer(str.length);
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < str.length; i++) {
        bytes[i] = str.charCodeAt(i);
    }
    return buffer;
}

// Convert backend options to PublicKeyCredentialCreationOptions
function parseCreationOptions(options) {
    options.challenge = base64urlToBuffer(options.challenge);
    options.user.id = base64urlToBuffer(options.user.id);
    if (options.excludeCredentials) {
        options.excludeCredentials.forEach((cred) => {
            cred.id = base64urlToBuffer(cred.id);
        });
    }
    return options;
}

// Convert backend options to PublicKeyCredentialRequestOptions
function parseRequestOptions(options) {
    options.challenge = base64urlToBuffer(options.challenge);
    if (options.allowCredentials) {
        options.allowCredentials.forEach((cred) => {
            cred.id = base64urlToBuffer(cred.id);
        });
    }
    return options;
}

// Format the resulting credential to send to the backend
function formatCreationResponse(credential) {
    return {
        id: credential.id,
        rawId: bufferToBase64url(credential.rawId),
        type: credential.type,
        response: {
            clientDataJSON: bufferToBase64url(credential.response.clientDataJSON),
            attestationObject: bufferToBase64url(credential.response.attestationObject),
            authenticatorData: credential.response.getAuthenticatorData ? bufferToBase64url(credential.response.getAuthenticatorData()) : undefined,
            transports: credential.response.getTransports ? credential.response.getTransports() : [],
            publicKeyAlgorithm: credential.response.getPublicKeyAlgorithm ? credential.response.getPublicKeyAlgorithm() : undefined,
            publicKey: credential.response.getPublicKey ? bufferToBase64url(credential.response.getPublicKey()) : undefined,
        },
    };
}

function formatRequestResponse(credential) {
    return {
        id: credential.id,
        rawId: bufferToBase64url(credential.rawId),
        type: credential.type,
        response: {
            clientDataJSON: bufferToBase64url(credential.response.clientDataJSON),
            authenticatorData: bufferToBase64url(credential.response.authenticatorData),
            signature: bufferToBase64url(credential.response.signature),
            userHandle: credential.response.userHandle ? bufferToBase64url(credential.response.userHandle) : null,
        },
    };
}

async function registerPasskey(challengeUrl, verifyUrl, csrfToken, deviceName) {
    try {
        // 1. Get challenge
        const resp = await fetch(challengeUrl, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/json" }
        });
        if (!resp.ok) throw new Error(await resp.text());
        const options = await resp.json();

        // 2. Call WebAuthn API
        const creationOptions = parseCreationOptions(options);
        const credential = await navigator.credentials.create({ publicKey: creationOptions });

        // 3. Send response to backend
        const responseData = formatCreationResponse(credential);
        responseData.device_name = deviceName;

        const verifyResp = await fetch(verifyUrl, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/json" },
            body: JSON.stringify(responseData),
        });

        if (!verifyResp.ok) throw new Error(await verifyResp.text());
        
        // Let HTMX handle any triggers by parsing headers if needed, 
        // or just fire custom event manually
        document.body.dispatchEvent(new Event("passkeyRegistered"));
        return true;
    } catch (err) {
        console.error(err);
        alert("Gagal mendaftarkan sidik jari/passkey: " + err.message);
        return false;
    }
}

async function loginPasskey(challengeUrl, verifyUrl, csrfToken) {
    try {
        // 1. Get challenge
        const resp = await fetch(challengeUrl, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/json" }
        });
        if (!resp.ok) throw new Error(await resp.text());
        const options = await resp.json();

        // 2. Call WebAuthn API
        const requestOptions = parseRequestOptions(options);
        const credential = await navigator.credentials.get({ publicKey: requestOptions });

        // 3. Send response to backend
        const responseData = formatRequestResponse(credential);

        const verifyResp = await fetch(verifyUrl, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/json" },
            body: JSON.stringify(responseData),
        });

        if (!verifyResp.ok) throw new Error(await verifyResp.text());
        
        // HTMX HX-Redirect header might be in response
        const hxRedirect = verifyResp.headers.get("HX-Redirect");
        if (hxRedirect) {
            window.location.href = hxRedirect;
        } else {
            window.location.reload();
        }
    } catch (err) {
        console.error(err);
        alert("Gagal login dengan biometrik: " + err.message);
    }
}

// Make globally available
window.registerPasskey = registerPasskey;
window.loginPasskey = loginPasskey;
