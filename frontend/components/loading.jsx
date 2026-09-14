// sometimes loading new cities and finding the venues might take a little bit so we need a cute loading text, like "Loading..." to display
// i want the loading text to be centered and styled nicely and to have each character jump or animate individually!
export default function Loading() {
    const loadingText = "Loading...";
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontSize: '2rem', fontWeight: 'bold' }}>
            {loadingText.split("").map((char, index) => (
                <span key={index} style={{ display: 'inline-block', animation: `jump 0.5s ease-in-out ${index * 0.1}s infinite` }}>
                    {char}
                </span>
            ))}
            <style jsx>{`
                @keyframes jump {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }
            `}</style>
        </div>
    );
}