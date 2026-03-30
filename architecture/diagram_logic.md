# Architecture Diagram Logic

The architecture diagram `diagram.png` (not included in this repository's source code) represents the following data flow:

1.  **PSTN / Customer Caller**: The entry point for the call.
2.  **Amazon Connect**: The core contact center platform.
    *   **Contact Flow**: Orchestrates the journey.
3.  **AWS Lambda (Customer Lookup)**: Triggered at the start.
    *   **Input**: Phone Number.
    *   **Output**: Customer Name, Membership Level.
4.  **Amazon DynamoDB**: Serves as the CRM backend.
5.  **Amazon Lex**: The NLU engine.
    *   **Input**: Voice stream (SRTP).
    *   **Output**: Intent Name, Confidence Score, Slots.
6.  **AWS Lambda (Routing Logic)**:
    *   **Input**: Lex Intent + Membership Level.
    *   **Output**: Target Queue ARN, Priority.
7.  **Amazon Connect (Queue & Agent)**: Final destination for the call.
8.  **Amazon CloudWatch**: For centralized logging and metrics.

---

### Visual Layout Recommendation:
- **Left**: User (Phone Icon).
- **Center**: Amazon Connect (Large box containing Lex and Lambda).
- **Right**: DynamoDB (Database icon) and CloudWatch (Logging icon).
- **Arrows**: Show the bi-directional communication between Connect and Lambda/Lex.
