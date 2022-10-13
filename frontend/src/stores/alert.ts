import { ref, computed } from "vue";
import { defineStore, acceptHMRUpdate } from "pinia";

const DEFAULT_TIMEOUT = 3500,
  MESSAGE_INFO = "info",
  MESSAGE_DANGER = "danger",
  MESSAGE_SUCCESS = "success",
  MESSAGE_WARNING = "warning";

type MessageLevel =
  | typeof MESSAGE_INFO
  | typeof MESSAGE_DANGER
  | typeof MESSAGE_SUCCESS
  | typeof MESSAGE_WARNING;

type Message = {
  body: string;
  timeout?: number;
  level: MessageLevel;
};

type AlertState = {
  messages: Message[];
};

const useAlertStore = defineStore("alert", {
  state: (): AlertState => ({
    messages: [],
  }),

  getters: {
    hasMessages(): boolean {
      return this.messages.length > 0;
    },
  },

  actions: {
    addMessage(message: Message) {
      this.messages.push(message);
      setTimeout(() => {
        this.removeMessage(this.messages.length - 1);
      }, message.timeout || DEFAULT_TIMEOUT);
    },

    removeMessage(message_idx: number) {
      this.messages.splice(message_idx, 1);
    },

    clearMessages() {
      this.messages = [];
    },

    alertInfoMsg(body: string, timeout: number = DEFAULT_TIMEOUT) {
      this.addMessage({ body, timeout, level: MESSAGE_INFO });
    },

    alertSuccessMsg(body: string, timeout: number = DEFAULT_TIMEOUT) {
      this.addMessage({ body, timeout, level: MESSAGE_SUCCESS });
    },

    alertWarningMsg(body: string, timeout: number = DEFAULT_TIMEOUT) {
      this.addMessage({ body, timeout, level: MESSAGE_WARNING });
    },

    alertDangerMsg(body: string, timeout: number = DEFAULT_TIMEOUT) {
      this.addMessage({ body, timeout, level: MESSAGE_DANGER });
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAlertStore, import.meta.hot));
}

export default useAlertStore;
