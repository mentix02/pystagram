export const setDocumentTitle = (title: string) => {
  document.title = `${title} | ${__VITE_ENV__.app_title}`;
};
