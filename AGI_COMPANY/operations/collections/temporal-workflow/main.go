package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
	"go.temporal.io/sdk/workflow"
)

func main() {
	c, err := client.Dial(client.Options{
		HostPort: "127.0.0.1:7233",
	})
	if err != nil {
		log.Fatalln("Unable to create client", err)
	}
	defer c.Close()

	w := worker.New(c, "collections-queue", worker.Options{})
	w.RegisterWorkflow(CollectionsWorkflow)
	w.RegisterActivity(LoadOverdueAccountsActivity)
	w.RegisterActivity(SendFriendlyReminderActivity)
	w.RegisterActivity(SendSecondNoticeActivity)
	w.RegisterActivity(SendFinalNoticeActivity)
	w.RegisterActivity(ReviewAccountActivity)
	w.RegisterActivity(LogCollectionActivity)

	log.Println("Starting collections worker...")
	if err := w.Run(worker.InterruptCh()); err != nil {
		log.Fatalln("Unable to start worker", err)
	}
}

// Account represents a customer account
type Account struct {
	ID        string
	Name      string
	Email     string
	Phone     string
	Amount    float64
	DueDate   string
	Stage     int // 0=new, 1=reminder, 2=second, 3=final, 4=review
	LastContact string
}

// CollectionsWorkflow: Main collections pipeline
func CollectionsWorkflow(ctx workflow.Context) error {
	logger := workflow.GetLogger(ctx)
	logger.Info("Starting collections workflow")

	ao := workflow.ActivityOptions{
		StartToCloseTimeout: 5 * time.Minute,
	}
	ctx = workflow.WithActivityOptions(ctx, ao)

	// Load overdue accounts from data source
	var accounts []Account
	err := workflow.ExecuteActivity(ctx, LoadOverdueAccountsActivity).Get(ctx, &accounts)
	if err != nil {
		return fmt.Errorf("load accounts failed: %w", err)
	}

	logger.Info("Loaded accounts", "count", len(accounts))

	// Process each account through stages
	for _, account := range accounts {
		err = processAccount(ctx, account)
		if err != nil {
			logger.Warn("Failed to process account", "id", account.ID, "error", err)
		}
	}

	logger.Info("Collections workflow complete")
	return nil
}

// processAccount handles one account through the stages
func processAccount(ctx workflow.Context, account Account) error {
	logger := workflow.GetLogger(ctx)

	switch account.Stage {
	case 0:
		// Stage 1: Friendly reminder
		err := workflow.ExecuteActivity(ctx, SendFriendlyReminderActivity, account).Get(ctx, nil)
		if err != nil {
			return err
		}
		logger.Info("Stage 1 complete", "account", account.ID)
		
		// Wait 1 day before next check
		workflow.Sleep(ctx, 24*time.Hour)

	case 1:
		// Stage 2: Second notice
		err := workflow.ExecuteActivity(ctx, SendSecondNoticeActivity, account).Get(ctx, nil)
		if err != nil {
			return err
		}
		logger.Info("Stage 2 complete", "account", account.ID)
		
		// Wait 7 days
		workflow.Sleep(ctx, 7*24*time.Hour)

	case 2:
		// Stage 3: Final notice
		err := workflow.ExecuteActivity(ctx, SendFinalNoticeActivity, account).Get(ctx, nil)
		if err != nil {
			return err
		}
		logger.Info("Stage 3 complete", "account", account.ID)
		
		// Wait 14 days
		workflow.Sleep(ctx, 14*24*time.Hour)

	case 3:
		// Stage 4: Account review
		err := workflow.ExecuteActivity(ctx, ReviewAccountActivity, account).Get(ctx, nil)
		if err != nil {
			return err
		}
		logger.Info("Stage 4 complete", "account", account.ID)
	}

	// Log the collection attempt
	return workflow.ExecuteActivity(ctx, LogCollectionActivity, account).Get(ctx, nil)
}

// LoadOverdueAccountsActivity: Read from Excel/Square
func LoadOverdueAccountsActivity(ctx context.Context) ([]Account, error) {
	// In production: read from Excel or Square API
	// For now: return sample data
	return []Account{
		{
			ID:      "ACC-001",
			Name:    "Acme Corp",
			Email:   "billing@acme.com",
			Phone:   "+1234567890",
			Amount:  1500.00,
			DueDate: "2026-06-01",
			Stage:   0,
		},
	}, nil
}

// SendFriendlyReminderActivity: Stage 1
func SendFriendlyReminderActivity(ctx context.Context, account Account) error {
	log.Printf("[C3P0] Sending friendly reminder to %s (%s)", account.Name, account.Email)
	// In production: send email/SMS
	return nil
}

// SendSecondNoticeActivity: Stage 2
func SendSecondNoticeActivity(ctx context.Context, account Account) error {
	log.Printf("[C3P0] Sending second notice to %s (%s)", account.Name, account.Email)
	return nil
}

// SendFinalNoticeActivity: Stage 3
func SendFinalNoticeActivity(ctx context.Context, account Account) error {
	log.Printf("[C3P0 + R2-D2] Sending FINAL notice to %s (%s)", account.Name, account.Email)
	return nil
}

// ReviewAccountActivity: Stage 4
func ReviewAccountActivity(ctx context.Context, account Account) error {
	log.Printf("[ALPHA-9] Account review for %s - recommending action", account.Name)
	// In production: analyze, recommend legal escalation or write-off
	return nil
}

// LogCollectionActivity: Record all attempts
func LogCollectionActivity(ctx context.Context, account Account) error {
	filename := "/root/.openclaw/workspace/memory/collections-log.md"
	content := fmt.Sprintf("- %s | %s | Stage %d | $%.2f\n", 
		time.Now().Format("2006-01-02 15:04"), account.Name, account.Stage, account.Amount)
	
	f, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer f.Close()
	_, err = f.WriteString(content)
	return err
}