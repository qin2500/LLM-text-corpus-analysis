css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}


'''

sys = '''
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
'''

user = '''
<div class="chat-message user">   
    <div class="message">{{MSG}}</div>
</div>
'''