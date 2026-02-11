import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [ posts, setPosts ] = useState([]);
  const [ title, setTitle ] = useState("");
  const [ content, setContent ] = useState("");
  const [ image, setImage ] = useState(null);
  
  const loadPosts = async () => {
    const res = await fetch (`${API}/posts`);
    const data = await res.json();
    setPosts(data);
  };

  useEffect(() => {
    loadPosts();
  }, []);

  const handleSubmit = async () => {
    const form = new FormData();

    form.append("title", title);
    form.append("content", content);
    if (image) form.append("image", image);

    await fetch (`${API}/posts`, {
      method: "POST",
      body: form
    });

    setTitle("");
    setContent("");
    setImage(null);

    loadPosts();
    
  };

  return (
    <div style={{ padding: 40, fontFamily: "sans-serif" }}>
      <h1>Blog App</h1>

      <h2>Create Post</h2>
      <input
        placeholder="Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <br /><br />

      <textarea
        placeholder="Content"
        value={content}
        onChange={e => setContent(e.target.value)}
      />
      <br /><br />

      <input
        type="file"
        onChange={e => setImage(e.target.files[0])}
      />
      <br /><br />

      <button onClick={handleSubmit}>Add Post</button>

      <hr />

      <h2>All Posts ({posts.length})</h2>

      {posts.map(p => (
        <div key={p.id} style={{
          border: "1px solid gray",
          padding: 10,
          marginBottom: 20
        }}>
          <h3>{p.title}</h3>
          <p>{p.content}</p>

          {p.image_url && (
            <img
              src={`${API}${p.image_url}`}
              width="300"
            />
          )}
          </div>
      ))}
      
    </div>
  )
}