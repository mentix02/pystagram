const HOST = import.meta.env.PROD ? "" : "http://localhost:8000";

const configureEndpoint = (endpoint: string) => `${HOST}/${endpoint}`;

export default configureEndpoint;
