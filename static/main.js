async function sendData() {
    const statusDiv = document.getElementById('status');
    const sendBtn = document.getElementById('sendButton');

    const token = document.getElementById('token').value.trim();
    const chat_id = document.getElementById('chat_id').value.trim();
    const text = document.getElementById('text').value.trim();

    if (!token || !chat_id || !text) {
        statusDiv.innerText = 'Заполните все поля!';
        return;
    }

    statusDiv.innerText = 'Запрос отправлен, пожалуйста, подождите...';
    if (sendBtn) sendBtn.disabled = true;

    const payload = {
        token,
        chat_id,
        message: { text }
    };
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
    const token = document.getElementById("token").value;
    if (!token) {
        document.getElementById("status").innerText = "Пожалуйста, введите токен бота.";
        return;
    }

    const formData = new FormData();
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
