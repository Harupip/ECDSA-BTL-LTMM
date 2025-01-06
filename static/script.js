async function generateKeys() {
    const response = await fetch('/generate_keys', { method: 'POST' });
    const data = await response.json();
    document.getElementById('keys').innerHTML = `
        <p class="text-break"><span class="font-bold">Private Key:</span> ${data.private_key}</p>
        <p class="text-break"><span class="font-bold">Public Key:</span> (${data.public_key.x}, ${data.public_key.y})</p>
        <p class="text-break"><span class="font-bold">Base Point:</span> (${data.base_point.x}, ${data.base_point.y})</p>
        <p class="text-break"><span class="font-bold">n:</span> ${data.n}</p>
    `;
}

async function signMessage() {
    const message = document.getElementById('message').value;
    const privateKey = prompt("Enter your private key:");
    const response = await fetch('/sign_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, private_key: privateKey })
    });
    const data = await response.json();
    console.log(data)
    document.getElementById('signature').innerHTML = `
        <p class="text-break"><span class="font-bold">Signature:</span> (r=${data.r}, s=${data.s})</p>
    `;
}

async function verifySignature() {
    const message = document.getElementById('verify-message').value;
    const r = document.getElementById('r').value;
    const s = document.getElementById('s').value;
    const useGeneratedKey = document.getElementById("useGeneratedKey").checked;
    let publicKey = null;

    if (!useGeneratedKey) {
        const x = document.getElementById("publicKeyX").value;
        const y = document.getElementById("publicKeyY").value;
        publicKey = { x: parseInt(x), y: parseInt(y) };
    }

    const response = await fetch('/verify_signature', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message, r, s, public_key: publicKey, use_generated_key: useGeneratedKey
        })
    });
    const data = await response.json();
    document.getElementById('verification-result').innerHTML = `
        <p>Verification Result: ${data.valid ? "Valid" : "Invalid"}</p>
    `;
}

document.getElementById("useGeneratedKey").addEventListener("change", function () {
    const customKeyInputs = document.getElementById("customKeyInputs");
    customKeyInputs.style.display = this.checked ? "none" : "block";
});