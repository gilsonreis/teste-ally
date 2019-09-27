# Teste Ally


- duplicar .env.dist e renomear para .env
- Ajustar os valores do .env, conforme banco local. Para desenvolvimento, foi utilizado PostgreSQL, na versão 10.
- Ajustar também o email e token para o PagSeguro. Foi testado apenas em ambiente de Sandbox.

- Para gerar os hashs do pagseguro, usar esse exemplo (https://jsfiddle.net/gilsonreis/e49xLgnm/6/)
  - execute http://127.0.0.1:8000/api/checkout/pagseguro/retornar-session-id, copie a session_id e cole no fiddle abaixo, no método _PagSeguroDirectPayment.setSessionId_ 
  - esse fiddle irá retornar o token do cartão de crédito e o hash do comprador, necessário para executar o checkout no pagseguro.
  - Os dados do cartão está no fiddle, no método _PagSeguroDirectPayment.createCardToken_. Para testar cartão inválido, basta informar algum número diferente no parametro cardNumber e observar no DevTools do navegador.
  
- No postman, executar com método post http://127.0.0.1:8000/api/checkout/pagseguro/realizar-pagamento/evento/{id_show}, onde id_show é a id do show na qual está se comprando o ingresso.
  - Passar via post card_token, sender_hash e id_usuario, na qual card_token e sender_hash são os valores gerados no fiddle e o id é algum usuário cadastrado no sistema.
  