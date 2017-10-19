export default function getEnv() {
    return {
        name: process.env.NODE_ENV ? process.env.NODE_ENV : 'development'
    };
}