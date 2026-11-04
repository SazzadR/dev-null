import { readFile, writeFile } from 'fs/promises';
import { v4 as uuid } from 'uuid';
import { Injectable } from '@nestjs/common';
import { CreateMessageDto } from './dto.js';
import type { MessageInterface } from './message.interface.js';

@Injectable()
export class MessagesRepository {
  private readonly fileName;

  constructor() {
    this.fileName = 'messages.json';
  }

  async listMessages(): Promise<MessageInterface[]> {
    try {
      const messages: Record<string, { message: string }> = JSON.parse(
        await readFile(this.fileName, 'utf8'),
      );
      let response: MessageInterface[] = [];

      for (const [id, message] of Object.entries(messages)) {
        response.push({
          id: id,
          message: message.message,
        });
      }

      return response;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') {
        throw error;
      }
    }

    return [];
  }

  async getMessage(id: string): Promise<MessageInterface | undefined> {
    const messages: Record<string, { message: string }> = JSON.parse(
      await readFile(this.fileName, 'utf8'),
    );
    for (const [messageId, message] of Object.entries(messages)) {
      if (id === messageId) {
        return {
          id: id,
          message: message.message,
        };
      }
    }
  }

  async createMessage(
    createMessageDto: CreateMessageDto,
  ): Promise<MessageInterface> {
    const id = uuid();
    let messages: Record<string, { message: string }> = {};

    try {
      messages = JSON.parse(await readFile(this.fileName, 'utf8'));
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') {
        throw error;
      }
    }

    messages[id] = { message: createMessageDto.message };
    await writeFile(this.fileName, JSON.stringify(messages));

    return { id, message: createMessageDto.message };
  }
}
