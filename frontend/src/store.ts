import { configureStore } from '@reduxjs/toolkit';
import { conversationSlice } from './conversation/conversationSlice';
import {
  prefListenerMiddleware,
  prefSlice,
} from './preferences/preferenceSlice';

const key = localStorage.getItem('DocsGPTApiKey');
const doc = localStorage.getItem('DocsGPTRecentDocs');

const store = configureStore({
  preloadedState: {
    preference: {
      apiKey: key ?? '',
      selectedDocs: doc !== null ? JSON.parse(doc) : null,
      sourceDocs: null,
    },
  },
  reducer: {
    preference: prefSlice.reducer,
    conversation: conversationSlice.reducer,
  },
  middleware: (getDefaultMiddleware) => [
    ...getDefaultMiddleware(),
    prefListenerMiddleware.middleware,
  ],
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
