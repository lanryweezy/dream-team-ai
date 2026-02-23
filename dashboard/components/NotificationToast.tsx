import React, { useState, useEffect } from 'react';

interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface NotificationToastProps {
  toasts: Toast[];
  onRemove: (id: string) => void;
}

const NotificationToast: React.FC<NotificationToastProps> = ({ toasts, onRemove }) => {
  useEffect(() => {
    toasts.forEach(toast => {
      if (toast.duration !== 0) {
        const timer = setTimeout(() => {
          onRemove(toast.id);
        }, toast.duration || 5000);

        return () => clearTimeout(timer);
      }
    });
  }, [toasts, onRemove]);

  const getToastStyle = (type: string) => {
    switch (type) {
      case 'success':
        return {
          icon: '✅',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          textColor: 'text-green-800',
          iconBg: 'bg-green-100'
        };
      case 'error':
        return {
          icon: '❌',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          textColor: 'text-red-800',
          iconBg: 'bg-red-100'
        };
      case 'warning':
        return {
          icon: '⚠️',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
          textColor: 'text-yellow-800',
          iconBg: 'bg-yellow-100'
        };
      default:
        return {
          icon: 'ℹ️',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          textColor: 'text-blue-800',
          iconBg: 'bg-blue-100'
        };
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => {
        const style = getToastStyle(toast.type);
        
        return (
          <div
            key={toast.id}
            className={`max-w-sm w-full ${style.bgColor} ${style.borderColor} border rounded-lg shadow-lg p-4 animate-slide-in`}
          >
            <div className="flex items-start space-x-3">
              <div className={`p-1 rounded-full ${style.iconBg}`}>
                <span className="text-sm">{style.icon}</span>
              </div>
              
              <div className="flex-1 min-w-0">
                <h4 className={`text-sm font-semibold ${style.textColor} mb-1`}>
                  {toast.title}
                </h4>
                <p className="text-xs text-gray-600 mb-2">
                  {toast.message}
                </p>
                
                {toast.action && (
                  <button
                    onClick={toast.action.onClick}
                    className="text-xs bg-white text-gray-700 px-3 py-1 rounded-full hover:bg-gray-50 transition-colors duration-200"
                  >
                    {toast.action.label}
                  </button>
                )}
              </div>
              
              <button
                onClick={() => onRemove(toast.id)}
                className="text-gray-400 hover:text-gray-600 text-sm"
              >
                ✕
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Toast Manager Hook
export const useToast = () => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = (toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    setToasts(prev => [...prev, { ...toast, id }]);
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  const showSuccess = (title: string, message: string, action?: Toast['action']) => {
    addToast({ type: 'success', title, message, action });
  };

  const showError = (title: string, message: string, action?: Toast['action']) => {
    addToast({ type: 'error', title, message, action });
  };

  const showWarning = (title: string, message: string, action?: Toast['action']) => {
    addToast({ type: 'warning', title, message, action });
  };

  const showInfo = (title: string, message: string, action?: Toast['action']) => {
    addToast({ type: 'info', title, message, action });
  };

  return {
    toasts,
    removeToast,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    ToastContainer: () => <NotificationToast toasts={toasts} onRemove={removeToast} />
  };
};

export default NotificationToast;