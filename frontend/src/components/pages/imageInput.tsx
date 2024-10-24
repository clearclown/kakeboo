// frontend/src/components/pages/imageInput.tsx

'use client'

import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import apiClient from '@/utils/api';  // APIクライアントのインポート

export function ImageInputComponent() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  // 画像が選択されたときの処理
  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedImage(event.target.files[0]);
    }
  };

  // フォームが送信されたときの処理
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedImage) return;

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await apiClient.post('/receipts/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('アップロード成功:', response.data);
    } catch (error) {
      console.error('アップロード中にエラーが発生しました:', error);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-blue-700 mb-8">画像入力</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input type="file" accept="image/*" onChange={handleImageChange} />
        {selectedImage && (
          <div>
            <img
              src={URL.createObjectURL(selectedImage)}
              alt="Selected receipt"
              className="max-w-md mx-auto mb-4"
            />
          </div>
        )}
        <Button type="submit">アップロード</Button>
      </form>
    </div>
  );
}

export default ImageInputComponent;