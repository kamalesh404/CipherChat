const status = document.getElementById('status');
const usernameEl = document.getElementById('username');
const connectBtn = document.getElementById('connectBtn');
const peerBox = document.getElementById('peerBox');
const peerEl = document.getElementById('peer');
const loadPeerBtn = document.getElementById('loadPeerBtn');
const peerKeyEl = document.getElementById('peerKey');
const messagesEl = document.getElementById('messages');
const msgInput = document.getElementById('msgInput');
const sendBtn = document.getElementById('sendBtn');

let ws = null;
let myPriv = null; // hex
let peerPub = null;

function addMsg(text, me=false){
  const d=document.createElement('div');
  d.className='msg'+(me?' me':'');
  d.textContent=text;
  messagesEl.appendChild(d);
  messagesEl.scrollTop=messagesEl.scrollHeight;
}

// For demo, generate keypair in browser via SubtleCrypto would need async.
// Here we use a placeholder: ask server for peer pub, and use a fixed demo key.
// Real app would store priv in IndexedDB and use WebCrypto for X25519.
connectBtn.onclick = async ()=>{
  const username = usernameEl.value.trim();
  if(!username) return;
  const proto = location.protocol==='https:'?'wss':'ws';
  ws = new WebSocket(`${proto}://${location.host}/v1/ws/${username}`);
  ws.onopen = ()=>{ status.textContent='connected as '+username; status.style.background='#3fb950'; peerBox.style.display='flex'; msgInput.disabled=false; sendBtn.disabled=false; };
  ws.onclose = ()=>{ status.textContent='disconnected'; status.style.background='#30363d'; };
  ws.onmessage = (ev)=>{
    const data=JSON.parse(ev.data);
    if(data.type==='message'){
      addMsg(`${data.payload.sender}: (encrypted) ${data.payload.nonce_ct.slice(0,24)}...`);
    }
  };
};

loadPeerBtn.onclick = async ()=>{
  const peer = peerEl.value.trim();
  if(!peer) return;
  const r=await fetch(`/v1/users/${peer}`);
  if(!r.ok){ peerKeyEl.textContent='not found'; return; }
  const j=await r.json();
  peerPub=j.public_key;
  peerKeyEl.textContent=peerPub.slice(0,16)+'…';
};

sendBtn.onclick = ()=>{
  if(!ws || ws.readyState!==1) return;
  const text=msgInput.value.trim();
  if(!text) return;
  // Demo: send as plaintext envelope; real app would encrypt with ECDH+AES-GCM here.
  // Server is agnostic — it just forwards nonce_ct.
  const payload={ sender: usernameEl.value.trim(), recipient: peerEl.value.trim(), nonce_ct: btoa(text), msg_no: Date.now() };
  ws.send(JSON.stringify({type:'message', payload}));
  addMsg('me: '+text, true);
  msgInput.value='';
};
msgInput.addEventListener('keydown', e=>{ if(e.key==='Enter') sendBtn.click(); });
