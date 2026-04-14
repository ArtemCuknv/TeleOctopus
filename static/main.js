async function sendData() {
    const statusDiv = document.getElementById('status');
    const sendBtn = document.getElementById('sendButton');

    const api_id = document.getElementById('api_id').value.trim();
    const api_hash = document.getElementById('api_hash').value.trim();
    const token = document.getElementById('token').value.trim();
    const chat_id = document.getElementById('chat_id').value.trim();
    const text = document.getElementById('text').value.trim();

    console.log(api_id)

    if (!api_id || !api_hash || !token || !chat_id || !text) {
        statusDiv.innerText = 'Заполните все поля!';
        return;
    }

    statusDiv.innerText = 'Запрос отправлен, пожалуйста, подождите...';
    if (sendBtn) sendBtn.disabled = true;

    const payload = {
        api_id,
        api_hash,
        token,
        chat_id,
        message: { text }
    };
    console.log('Sending payload:', payload);
    try {
        const response = await fetch('/send_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        console.log(result);

        if (result.status == "ok") {
            statusDiv.innerText = 'Сообщение успешно отправлено!';
        } else {
            statusDiv.innerText = 'Ошибка: ' + (result.error || 'Неизвестная ошибка');
        }
    } catch (error) {
        statusDiv.innerText = 'Ошибка запроса: ' + error;
    } finally {
        if (sendBtn) sendBtn.disabled = false;
    }
}

async function addBot() {
    const api_id = document.getElementById("api_id").value.trim();
    const api_hash = document.getElementById("api_hash").value.trim();
    const token = document.getElementById("token").value.trim();

    if (!api_id || !api_hash || !token) {
        document.getElementById("status").innerText = "Заполните все поля!";
        return;
    }

    const formData = new FormData();
    formData.append("api_id", api_id);
    formData.append("api_hash", api_hash);
    formData.append("token", token);

    try {
        const response = await fetch("/add_bot_post", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (result.status === "ok") {
            document.getElementById("status").innerText = "Бот успешно добавлен!";
            document.getElementById("token").value = ""; // Очистить поле
        } else {
            document.getElementById("status").innerText = "Ошибка: " + (result.error || "Неизвестная ошибка");
        }
    } catch (error) {
        document.getElementById("status").innerText = "Ошибка сети: " + error.message;
    }
}
