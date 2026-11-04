import { Injectable } from '@nestjs/common';
import { MessagesRepository } from './messages.repository.js';
import { CreateMessageDto } from './dto.js';
import type { MessageInterface } from './message.interface.js';

@Injectable()
export class MessagesService {
  constructor(public readonly messagesRepository: MessagesRepository) {}

  listMessages(): Promise<MessageInterface[]> {
    return this.messagesRepository.listMessages();
  }

  getMessage(id: string): Promise<MessageInterface | undefined> {
    return this.messagesRepository.getMessage(id);
  }

  createMessage(createMessageDto: CreateMessageDto): Promise<MessageInterface> {
    return this.messagesRepository.createMessage(createMessageDto);
  }
}
